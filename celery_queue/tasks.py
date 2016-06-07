# -*- coding: utf-8 -*-
from __future__ import absolute_import
from openerp.tools import config
from celery import Celery
from kombu import Exchange, Queue
import logging

celery = Celery('celery_queue')
celery_default_queue = config.get('celery_default_queue', 'openerp')
celery_queues = config.get('celery_queues', "")

_logger = logging.getLogger("Celery")


class CeleryConfig():
    BROKER_URL = config.get('celery_broker_url')
    CELERY_DEFAULT_QUEUE = celery_default_queue
    CELERY_QUEUES = (
        Queue(celery_default_queue, Exchange(celery_default_queue),
              routing_key=celery_default_queue),
    )
    for queue in filter(lambda q: q.strip(), celery_queues.split(",")):
        CELERY_QUEUES = CELERY_QUEUES + \
            (Queue(queue, Exchange(queue), routing_key=queue),)


celery.config_from_object(CeleryConfig)


@celery.task(name='openerp.addons.celery_queue.tasks.execute')
def execute(conf_attrs, dbname, uid, obj, method, *args, **kwargs):
    import openerp
    from openerp.api import Environment
    from openerp.modules.registry import Registry
    for attr, value in conf_attrs.items():
        openerp.tools.config[attr] = value
    with Environment.manage():
        registry = Registry(dbname)
        cr = registry.cursor()
        context = kwargs.pop('context') or {}
        env = Environment(cr, uid, context)
        # openerp.api.Environment._local.environments = env
        try:
            getattr(env.registry[obj], method)(cr, uid, *args, **kwargs)
        except Exception as exc:
            env.cr.rollback()
            try:
                raise execute.retry(
                    queue=execute.request.delivery_info['routing_key'],
                    exc=exc, countdown=(execute.request.retries + 1) * 60,
                    max_retries=5)
            except Exception as retry_exc:
                raise retry_exc
        finally:
            env.cr.commit()
            env.cr.close()
    return True
