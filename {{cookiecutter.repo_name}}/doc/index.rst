.. toctree::
   :hidden:

   developer
   {{ cookiecutter.repo_name }}/{{ cookiecutter.repo_name }}

{{ '=' * cookiecutter.project_name|length }}
{{ cookiecutter.project_name }}
{{ '=' * cookiecutter.project_name|length }}

.. container:: float-right

   .. image:: _static/images/logo.png

{{ cookiecutter.short_description|wordwrap(79) }}


Documentation
=============

- :doc:`Developer Guide. <developer>`
- :doc:`Internal Documentation Reference. <{{ cookiecutter.repo_name }}/{{ cookiecutter.repo_name }}>`


Development
===========

- `Project repository. <{{ cookiecutter.repo_url }}>`_


License
=======

::

   Copyright (C) {{ cookiecutter.year }} {{ cookiecutter.author }}

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing,
   software distributed under the License is distributed on an
   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
   KIND, either express or implied.  See the License for the
   specific language governing permissions and limitations
   under the License.
