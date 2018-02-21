# Pivotal Cloud Foundry for Drupal 8

This tutorial will help you run Drupal 8 on Pivotal Cloud Foundry (PCF). PCF is a tool to help you run continuous integration on your own private cloud. With PCF you can easily spin off new development environments and new projects through the use of a powerful GUI.

This is an example of Drupal 8 application which can be ran on Pivotal Cloud Foundry using the PHP Build Pack. Drupal installation is based on Composer template for Drupal projects Official buildpack documentation can be found at: http://docs.cloudfoundry.org/buildpacks/php/index.htm

## PCF Template for Drupal 8

First step will be to clone our template for a Drupal 8 application with Composer.

  ```bash
  git clone git@github.com:softescu/pcf-drupal-8.git pcf-drupal-8
  ```
The template has the following directories:
  - `.bp-config` contains PHP and Httpd configuration
  - `.extensions` contains non-core extensions (MySQL and Drush)
  - `drush` this folder is required for Drush extension installation
  - `htdocs` this folder will be Web Directory for the application, contains: custom modules, custom themes, custom profiles, etc.
  - `mysql` this folder is required for MySQL extension installation
  - `scripts` contains an autoloadable class for composer

## Template Features

At the time of writing this blog post, the PCF Drupal 8 template delivers the following features:
  - PHP Version 7.0.26
  - Drush Version 8.1.15
  - MySQL Client Version 5.7.20
  - Drupal Version 8.4.3
  - Drupal Simple OAuth Version 3.0
  - Drupal s3fs Version ^3.0@alpha
  - Use of S3 bucket for files storage
  - OAuth installed in Drupal

<b>PHP Extensions and Modules:</b>

  - OP Cache
  - Gzip output
  - MySQLnd (MySQL Native Driver)
  - MySQLi (MySQL Improved Extension)
  - PDO
  - PDO_MYSQL (MySQL Functions)
  - Session
  - cURL
  - MbString (Multibyte String)
  - ImageMagick (Image Processing)

## How to deploy Drupal 8 to PCF?

This tutorial assumes that you already have Pivotal Cloud Foundry installed and running. First step will be to clone our template for a Drupal 8 application with Composer with:

  ```bash
  git clone git@github.com:softescu/pcf-drupal-8.git pcf-drupal-8
  ```

### You need to create an MySQL service instance in PCF.
  ```bash
  cf create-service p-mysql <plan name> drupal-8-pcf-db
  ```

### Push it to CloudFoundry.
  ```bash
  cf push
  ```

### Configure Drupal 8

Once the command `cf push` has finished, your repo is pushed to your target PCF application. Drupal dependencies are automatically installed with Composer.
More about how composer dependencies are managed inside PCF linux container you can <a target="_blank" href="https://docs.cloudfoundry.org/buildpacks/php/gsg-php-composer.html">see here.</a>

Drupal will be installed inside your web directory `htdocs`. Contrib Modules (packages of type drupal-module) will be placed in `htdocs/modules/contrib/`. Contrib Theme (packages of type drupal-theme) will be placed in `htdocs/themes/contrib/`. Contrib Profiles (packages of type drupal-profile) will be placed in `htdocs/profiles/contrib/`. The `htdocs/sites/default/files` directory is automatically created.

Once the initial push has been finished, you should continue and finish to install Drupal by accessing your application domain name and follow the D8 installation wizard.

### Configure Simple OAuth

Our template already contains the modules necessary to run OAuth with D8.
Go to "/admin/config/people/simple_oauth" and save the path to your keys. Keys are generated automatically to this location `/home/vcap/app/cert` by the oauth extension `.extensions/oauth`

You can read more info how to configure <a target="_blank" href="https://www.drupal.org/project/simple_oauth">Simple OAuth.</a>

### Configure Drupal File System with S3

File system must be stored to Amazon Simple Cloud Storage Service‎ (S3). Applications running on Cloud Foundry should not write files to the local file system for the following reason:

<b>Local file system storage is short-lived.</b> When an application instance crashes or stops, the resources assigned to that instance are reclaimed by the platform including any local disk changes made since the app started. When the instance is restarted, the application will start with a new disk image. Although your application can write local files while it is running, the files will disappear after the application restarts.

<b>Drupal S3 File System</b> (s3fs) provides an additional file system to your drupal site, which stores files in Amazon's Simple Storage Service (S3) or any other S3-compatible storage service.

To configure Drupal s3fs module the following details about AWS S3 Service are required:
  - Amazon Web Service Access Key
  - Amazon Web Service Secret Key
  - S3 Bucket Name
  - S3 Region

<b>Setup steps:</b>
  - Setup your credentials in the Drupal configuration page for the s3fs module “/admin/config/media/s3fs”
  - Configure the Drupal File System destination in the File System configuration page “/admin/config/media/file-system” by choosing “Amazon Simple Storage Service” option.

### Configure Drupal database for PCF MySQL Service

Cloud Foundry adds connection details to the `VCAP_SERVICES` environment variable when you restart your application, after binding a service instance to your application. The results are returned as a JSON document that contains an object for each service for which one or more instances are bound to the application.

Database credentials can be readed by parsing JSON Object stored in `VCAP_SERVICES` environment variable.

Example:

  ```bash
  $services = getenv("VCAP_SERVICES");
  $services_json = json_decode($services,true);
  $mysql_config = $services_json["p-mysql"][0]["credentials"];

  ```

To connect your Drupal 8 application, we’ve already done the settings in `settings.php`.

## Advanced options for the PCF Drupal 8 template

### Customize Application Attributes

The template offers several options to customize your application with the manifest.

Configuration file: `manifest.yml`
  - `name` attribute to specify name for your app instance
  - `buildpack` attribute to specify Github URL for PHP buildpack
  - `disk_quota` attribute to specify the disk space for your app instance
  - `memory` attribute to specify the memory limit for your app instance
  - `services` attribute to specify the services list for your app instance

### Adding  extension for PHP Buildpack

In CloudFoundry an extensions is a set of Python methods that will get called during the staging process and will install precompiled packages. To create an extension, simply create a folder in the `.extensions` folder.

The name of the folder will be the name of the extension. Inside the newly created folder, create a file called `extension.py`. That file will contain your code. Inside that file, put your extension methods and any additional required code.

The following extensions already exist in our template file:
  - `.extensions/drush` install and configure Drush inside cflinuxfs2 Linux container
  - `.extensions/mysql` install MySQL Client inside cflinuxfs2 Linux container
  - `.extensions/oauth` install key pairs required for the Simple OAuth Drupal module

## Advanced PHP Buildpack Configurations

Pivotal Cloud Foundry (PCF) documentation at PHP Buildpack Configuration can be <a hef="https://docs.cloudfoundry.org/buildpacks/php/gsg-php-config.html" target="_blank">read here.</a> The buildpack overrides the default `options.json` file with any configuration it finds in the `.bp-config/options.json` file of your application.

The buildpack will add any `.bp-config/php/fpm.d` files it finds in the application to the PHP-FPM configuration. This can be used to change any value which is acceptable to php-fpm.ini

The buildpack will add any `.bp-config/php/php.ini.d/<file>.ini` files it finds in the application to the PHP configuration. For example, this can be used to enable PHP or ZEND extensions

## PHP configuration for Drupal 8

A list of available PHP versions, extensions and modules can be found <a href="https://github.com/cloudfoundry/php-buildpack/releases" target="_blank">here.</a>
By default, our Drupal 8 template contains in `.bp-config/options.json` the following options:
  - PHP Version: 7.0.26
  - PHP Extensions: bz2, curl, dba, gd, imagick, imap, mbstring, mysqli, opcache, openssl, pdo, pdo_mysql, pdo_odbc, sockets, xsl, zip, zlib
  - PHP Modules: pear, fpm, cli

## PHP Opcache configuration

PHP Opcache configuration with recommended php.ini settings were added here: `.bp-config/php/php.ini.d/extra.ini`

  ```bash
  [opcache]
  opcache.enable=1
  opcache.memory_consumption=128
  opcache.interned_strings_buffer=8
  opcache.max_accelerated_files=4000
  opcache.revalidate_freq=60
  opcache.fast_shutdown=1
  opcache.enable_cli=1

  ```

## PHP FastCGI configuration

PHP-FPM pool configuration settings are here: `.bp-config/php/fpm.d/extra.conf`
List of global php-fpm.conf directives can be found <a href="http://php.net/manual/en/install.fpm.configuration.php" target="_blank">here.</a>

