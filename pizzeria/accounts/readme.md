# Accounts

## General info

This application handles logging in, logging out, and creating accounts for
new users. All of the User accounts are standard Django User objects.

### Requirements / General Notes

All of the templates {% extends 'layout.html' %} which accepts a *body* block,
and a *footer_navbar* block as blocks that change.