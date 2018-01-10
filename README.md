# Pivotal Cloud Foundry for Drupal 8

This is an example of Drupal 8 application which can be ran on Pivotal Cloud Foundry using the [PHP Build Pack]. Drupal installation is based on <a href="https://github.com/drupal-composer/drupal-project">Composer template for Drupal projects</a>

## Buildpack User Documentation

Official buildpack documentation can be found at http://docs.cloudfoundry.org/buildpacks/php/index.html

## Usage

#### Deploy Application

1. Clone this repo.

  ```bash
  git clone git@github.com:softescu/pcf-drupal-8.git pcf-drupal-8
  cd pcf-drupal-8
  ```

2. Create a <a href="http://docs.pivotal.io/p-mysql/2-0/use.html">MySQL</a> service.

  ```bash
  cf create-service p-mysql <plan name> drupal-8-pcf-db
  ```

3. Push it to CloudFoundry.

  ```bash
  cf push
  ```
#### Install Drupal and configure Simple OAuth
1. Install Drupal by accessing your application domain name
2. Go to `/admin/config/people/simple_oauth` and save the path to your keys. Keys are generated to this location `/home/vcap/app/cert` by oauth extension `.extensions/oauth`
    - Read more info how to configure <a href="https://www.drupal.org/project/simple_oauth">Simple OAuth</a>

## How It Works
1. The local code is pushed to your target PCF application. Drupal dependencies are installed with Composer.
More about how composer dependencies are managed inside PCF linux container you can see <a href="https://docs.cloudfoundry.org/buildpacks/php/gsg-php-composer.html">here</a>
2. Drupal will be installed inside your web directory `htdocs`
3. Contrib Modules (packages of type drupal-module) will be placed in `htdocs/modules/contrib/`
4. Contrib Theme (packages of type drupal-theme) will be placed in `htdocs/themes/contrib/`
5. Contrib Profiles (packages of type drupal-profile) will be placed in `htdocs/profiles/contrib/`
6. The `htdocs/sites/default/files` directory is automatically created


## Customize Application Attributes

<a href="https://docs.cloudfoundry.org/devguide/deploy-apps/manifest.html">Manifest Configuration</a> `manifest.yml`

  - `- name` attribute to specify name for your app instance
  - `buildpack` attribute to specify Github URL for PHP buildpack
  - `disk_quota` attribute to specify the disk space for your app instance
  - `memory` attribute to specify the memory limit for your app instance
  - `services` attribute to specify the services list for your app instance

<a href="https://github.com/cloudfoundry/php-buildpack">CloudFoundry extension for PHP Buildpack</a> `.extensions`
Examples:

  - `drush` install and configure <a href="https://github.com/drush-ops/drush">Drush</a> inside <a href="https://github.com/cloudfoundry/cflinuxfs2">cflinuxfs2</a> Linux container
  - `mysql` install <a href="https://dev.mysql.com/doc/mysql-sourcebuild-excerpt/5.5/en/installing-source-distribution.html">MySQL Client</a> inside <a href="https://github.com/cloudfoundry/cflinuxfs2">cflinuxfs2</a> Linux container

## PHP Buildpack Configuration

Pivotal Cloud Foundry (PCF) documentation at <a href="https://docs.cloudfoundry.org/buildpacks/php/gsg-php-config.html">PHP Buildpack Configuration</a>

  - The buildpack overrides the default `options.json` file with any configuration it finds in the `.bp-config/options.json` file of your application
  - The buildpack will add any `.bp-config/php/fpm.d` files it finds in the application to the PHP-FPM configuration. This can bes used to change any value which is acceptable to `php-fpm.ini`
  - The buildpack will add any `.bp-config/php/php.ini.d/<file>.ini` files it finds in the application to the PHP configuration. This can be used to enable PHP or ZEND extensions

## PHP configuration for <a href="https://www.drupal.org/docs/8/system-requirements/php#drupalversions">Drupal 8</a>

A list of available PHP versions, extensions and modules can be found <a href="https://github.com/cloudfoundry/php-buildpack/releases">here.</a>
 File `.bp-config/options.json` contains:

  ```bash
  - PHP Version: 7.0.26
  - PHP Extensions: bz2, curl, dba, gd, imagick, imap, mbstring, mysqli, opcache, openssl, pdo, pdo_mysql, pdo_odbc, sockets, xsl, zip, zlib
  - PHP Modules: pear, fpm, cli
  ```
PHP Opcache configuration with <a href="http://php.net/manual/ro/opcache.installation.php#opcache.installation.recommended">recommended php.ini settings</a>: `.bp-config/php/php.ini.d/extra.ini`

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

PHP-FPM pool configuration: `.bp-config/php/fpm.d/extra.conf`
List of global php-fpm.conf directives can be found <a href="http://php.net/manual/en/install.fpm.configuration.php">here.</a>

## Project Structure

  The project is broken down into the following directories:
  - `.bp-config` contains PHP and Httpd configuration
  - `.extensions` contains non-core extensions (MySQL and Drush)
  - `drush` this folder is required for Drush extension installation
  - `htdocs` this folder will be Web Directory for the application, contains: custom modules, custom themes, custom profiles, etc..
  - `mysql` this folder is required for MySQL extension installation
  - `cert` this folder is required for key pair generation
  - `scripts` contains autoloadable class for composer