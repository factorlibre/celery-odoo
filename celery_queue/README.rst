.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

============
Celery Queue
============

This is the base module for the execution of Odoo tasks in a celery queue

Installation
============

To use this module, is necesary to install and configure celery python library

.. code:: python

    pip install celery

For more info on celery configuration and execution go to http://www.celeryproject.org/

Configuration
=============

To configure this module, you need to change some params in the odoo config file:

* celery_broker_url this param is used to connect celery with a message broker. For example for the default config with celery and rabbitmq:

    celery_broker_url=ampq://guest@localhost:5672/

* celery_default_queue this param is used to define the name of the queue used in the message broker. By default is openerp

    celery_default_queue=openerp

Usage
=====

This module is intented to be inherited by other modules as by itself it doesn't do nothing.

Example for use with other modules:

.. code:: python

    from openerp import api, models
    from openerp.addons.celery_queue.decorators import CeleryTask

    class ResPartner(models.Model):
        _inherit = 'res.partner'

        @CeleryTask()  # This decorator is the one that defines that this method is going to be enqueued in celery
        @api.multi
        def heavy_function(self):
            return super(ResPartner, self).heavy_function()

For task execution in celery is necessary to start a celery worker, for start the
worker is necessary to include the addon path and odoo path in PYTHONPATH. Example:

.. code:: bash

    export PYTHONPATH="/opt/odoo/odoo-server:/opt/odoo/modules/celery-dooo"
    celery -A celery_queue.tasks worker -c 1 -Q openerp

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/factorlibre/celery-odoo/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Hugo Santos <hugo.santos@factorlibre.com>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.