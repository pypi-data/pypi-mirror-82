# Group Assigner

Simple plugin for [AllianceAuth](https://gitlab.com/allianceauth/allianceauth) to assign groups to users when they change states.

## Installation
1. `pip install allianceauth-group-assigner`
2. add `'groupassign',` to your `INSTALLED_APPS` in the local.py, 
3. run migrations
4. restart auth

## Setup
* Add groups to the required State in admin `admin/groupassign/stategroupbinding/`
* this module will not remove groups
    * you can achieve this with the groups state permissions.

* If you wish to sync you existing users there is a task that can be setup.
    1. In Django Admin select periodic tasks
    2. Click Add New
    3. Se the name to Something meaning full "Sync all State Group Bindings"
    4. Pick `groupassign.tasks.check_all_bindings`from the task drop down
    5. Ensure Enabled is checked
    6. Click The green arrow inline with the crontab schedule to add a new cron.
    6. Set the cron to: Minutes `0`, Hours `0`, Days of the Week `0`, rest leave as `*` this will run the updates first day of each week at GMT 0000 (Or set it to what ever timer you like)
    7. Click Save on the cron window.
    8. Click save on The Periodic task.
    9. select the new task and pick `Run Selected Task` from the dropdown at the top and click `Go`

## Contributing
Make sure you have signed the [License Agreement](https://developers.eveonline.com/resource/license-agreement) by logging in at https://developers.eveonline.com before submitting any pull requests. All bug fixes or features must not include extra superfluous formatting changes. If you have an issue with formatting, push it in it's own PR for discussion. 

## Change log
* v0.0.1
  * First release