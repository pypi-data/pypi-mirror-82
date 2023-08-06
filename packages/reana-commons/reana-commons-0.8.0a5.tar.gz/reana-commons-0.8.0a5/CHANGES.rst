Changes
=======

Version master (UNRELEASED)
---------------------------

- Adds `get_disk_usage` utility function to calculate disk usage for a directory.
- Centralises `fs` package dependency

Version 0.7.0 (UNRELEASED)
---------------------------

- Adds new utility to send emails.
- Adds centralised operational options validation.
- Fixes memory leak in Bravado client instantiation. (`reanahub/reana-server#225 <https://github.com/reanahub/reana-server/issues/225>`_)
- Makes maximum number of running workflows configurable.
- Adds configurable prefix for component names.
- Adds central variable for the runtime pods node selector label.
- Allows specifying unpacked Docker images.
- Upgrades minimum version of Kubernetes Python library to 11.
- Centralises CephFS PVC name.
- Updates to latest CVMFS CSI driver.
- Introduces new configuration variable ``REANA_INFRASTRUCTURE_KUBERNETES_NAMESPACE`` to define the Kubernetes namespace in which REANA infrastructure components run.
- Introduces new configuration variable ``REANA_RUNTIME_KUBERNETES_NAMESPACE`` to define the Kubernetes namespace in which REANA runtime components components run.
- Increases default log level to ``INFO``.
- Add Black formatter support.
- Adds initfiles as an operational option for Yadage.

Version 0.6.1 (2020-05-25)
--------------------------

- Upgrades Kubernetes Python client.

Version 0.6.0 (2019-12-19)
--------------------------

- Adds new API for Gitlab integration.
- Adds new Kubernetes client API for ingresses.
- Adds new APIs for management of user secrets.
- Adds EOS storage Kubernetes configuration.
- Adds HTCondor and Slurm compute backends.
- Adds support for streaming file uploads.
- Allows unpacked CVMFS and CMS open data volumes.
- Adds Serial workflow step name and compute backend.
- Adds support for Python 3.8.

Version 0.5.0 (2019-04-16)
--------------------------

- Centralises log level and log format configuration.
- Adds new utility to inspect the disk usage on a given workspace.
  (``get_workspace_disk_usage``)
- Introduces the module to share Celery tasks accross REANA
  components. (``tasks.py``)
- Introduces common Celery task to determine whether REANA can
  execute new workflows depending on a set of conditions
  such as running job count. (``reana_ready``, ``check_predefined_conditions``,
  ``check_running_job_count``)
- Allows the AMQP consumer to be configurable with multiple queues.
- Introduces new queue for workflow submission. (``workflow-submission``)
- Introduces new publisher for workflow submissions.
  (``WorkflowSubmissionPublisher``)
- Centralises Kubernetes API client configuration and initialisation.
- Adds Kubernetes specific configuration for CVMFS volumes as utils.
- Introduces a new method, ``copy_openapi_specs``, to automatically move
  validated OpenAPI specifications from components to REANA Commons
  ``openapi_specifications`` directory.
- Centralises interactive session types.
- Introduces central REANA errors through the ``errors.py`` module.
- Skips SSL verification for all HTTPS requests performed with the
  ``BaseAPIClient``.

Version 0.4.0 (2018-11-06)
--------------------------

- Aggregates OpenAPI specifications of REANA components.
- Improves AMQP re-connection handling. Switches from ``pika`` to ``kombu``.
- Enhances test suite and increases code coverage.
- Changes license to MIT.

Version 0.3.1 (2018-09-04)
--------------------------

- Adds parameter expansion and validation utilities for parametrised Serial
  workflows.

Version 0.3.0 (2018-08-10)
--------------------------

- Initial public release.
- Provides basic AMQP pub/sub methods for REANA components.
- Utilities for caching used in different REANA components.
- Click formatting helpers.

.. admonition:: Please beware

   Please note that REANA is in an early alpha stage of its development. The
   developer preview releases are meant for early adopters and testers. Please
   don't rely on released versions for any production purposes yet.
