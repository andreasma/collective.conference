.. contents::

Introduction
============

The goal of this Plone add-on is to provide a framework for the organization of a conference.

The add-on creates a content type speaker inside a speaker folder. The speaker folder could be
created at every place on the Plone site. A speaker is restricted to a speaker folder.

There are also a section for call for papers. This section could be made only from site admins.
The potential speakers will then create new papers (talks or workshops) inside this section. The
papers - talks or workshops - will be reviewed in the cfp section and copied over later to the
track sessions of the program, if they get a slot inside one of the tracks of the program.

The program shows a title and descriptions and also its dates. The tracks could be created
inside the program and will get special title and descriptions. They have to fit inside the
program timeslot and will contain talks and workshops. The talks and workshops have title and
description. They get a length (in minutes) and an order id. This information will be used
to get them in the right order to the tracks (and at least to the program) and set the starting
and end time of every talk or workshop inside the program.

The add-on is currently in a pre-alpha status and there are some of the above features missing.
The development of this missing features is going on and help would be appreciated.
