<h1>Django Social Web Application</h1>

<p>This project is a Django-based social web application. Follow the steps below to clone and set up the project for development and production environments.</p>

<h2>Clone the Repository</h2>
<pre>
git clone https://github.com/mjavadvali/Django-social-web-application.git
</pre>

<p>Navigate to the project directory:</p>
<pre>
cd Django-social-web-application
</pre>

<h2>Production Setup</h2>

<h3>Generate a Django Secret Key</h3>
<p>Inside a Python shell, run the following command to generate a new Django Secret Key:</p>
<pre>
from django.core.management.utils import get_random_secret_key
get_random_secret_key()
</pre>

<p>Navigate to the <code>book-appointment</code> directory:</p>
<pre>
cd book-appointment
</pre>

<p>Open your <code>.env</code> file located inside the <code>django_social/env/.env</code> directory and replace the <code>SECRET_KEY</code> value with the generated key.</p>

<h2>Development Setup</h2>

<p>To set up the development environment, run the following command:</p>
<pre>
docker-compose -f docker-compose.dev.yml up --build
</pre>
