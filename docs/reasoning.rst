.. _reasoning:

Accepting Insanity
==================

The short of it is that I was fed up with all the tools out there.  Ticket
tracking wasn't working well enough.  Wiki's lacked a decent structure, and I
was always changin what structure I had created.  Word processors are a
nightmare.  I won't subject myself to MS Project [#]_. Text files crate
unmanageble sprawl. However, the biggest reason for my dissastisfaction was
that web browsers suck for data entry.  Espcially structured textual data.

I'm a vim user.  I like vim, I'm comfortable with vim, and, while not an
expert, I'm pretty handy when it comes to text manipulation.  I can easily cut
and paste, indent whole blocks of text, create macros to repeatedly perform
some operation, etc. and I don't have to use the mouse.  Emacs will do all
this for you too.  A web browser won't (neither will most word processores).
I am also dealing with lots of code, config files, command line entries, etc.
Text editors were *made* for this stuff.

I'm a git user.  Again, I'm not a powerful git user, but I know enough to
semi-effective.  Git is wonderful at merging changes from different locations.
Additionally, since it's a DVCS, I don't need access to the *server* in order
to save changes and revisions.  Using `gitosis
<http://scie.nti.st/2007/11/14/hosting-git-repositories-the-easy-and-secure-way>`
I can have a central repository that acts as my backup and *canonical* copy.
This makes it easy for me to update projects and tasks on my workstation or
laptop, regardless of where I am or what kind of connection I have.

I also like the expressiveness of ReST and the nice documents `sphinx
<http://sphinx.pocoo.org>`  creates.

So, in summary, the reasons I chose to use ReST and Git for project and task
managemnt are:

* Vim [#]_ is better than any web browser for text entry
* Git provides:

  * Anywhere access: different machines and operating systems
  * Acts as a backup
  * Has hooks for publishing locally or "publicly" on commit / push

* Sphinx creates pretty docs
* ReST is easy enough to learn and clear enough to read "un-rendered"
* ReST documents provide the flexibilty and formatting to producs good project
  and task documentaiton.



.. rubic:: Footnotes

.. [#]: MS Project is overkill for most of what I have to do, and it ties me
         to windows, which is another undesirable attribute.

.. [#]: Any text editor is pretty much better than a web browser for entering
         text.  I just happen to like vim.
