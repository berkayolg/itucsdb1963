Parts Implemented by Uğur Ali Kaplan
================================

Here, you will be able to find information about how to interact
with different pages of our website, SİS++ using various web forms.

Focus of this document is going to be these pages:

* Papers
* Labs
* Faculties
* Departments
* Clubs
* Buildings
* Assistants

Actually, all of these have the same logic. So, if you understand how
to use one, you will be able to understand how to use the others except
for the form you have to use when dealing with papers.

Let's start with the complicated one, papers.

1. Papers
--------------

Papers, as you can guess from its name lets you learn about various
authors and their papers.

If you were to go into papers page, you will see a box that asks you
to pick an author. Then, if a name in the database has papers, you will
be able to see their names in this list and learn more about their papers.

.. figure:: kaplan/papers.png
	:scale: 70 %
	:alt: Picking Author
	:align: center

If a person does not have a paper registered in the database, you will not
be able to see their name in this list.

After picking an author, you can see their papers listed as shown here:

.. figure:: kaplan/papersule.png
	:scale: 70 %
	:alt: Papers by author
	:align: center

Now, you can pick an entry from this table and hit delete or update. If you
hit delete and you have multiple authors, you will see that paper is still in
the database yet its authors does not include the author you have used to 
reach this listing.

As an example, let's say you choose "Uğur Ali Kaplan" as the author. And you
pick a paper, with authors "Uğur Ali Kaplan", "Berkay Olgun" and "Mehmet Altuner".
If you delete this paper, now when you pick "Berkay Olgun" as the author, you will
still be able to see the paper. What is different is however, that you will not
see "Uğur Ali Kaplan"s name listed along names of "Berkay Olgun" and "Mehmet Altuner".

Other than that, if you choose to update the papers, you will meet with a screen
such as the one below:

.. figure:: kaplan/updatepaper.png
	:scale: 70 %
	:alt: Paper update
	:align: center

As in the case of deleting, changes you make in paper updates are local. So, if you change the name
of the paper, name of the paper will only be different for this author and other entries
will not be affected.

As it is the case for all the other tables, if you wish to create an entry for papers you
will have to use the super user page.

.. figure:: kaplan/papercreate.png
	:scale: 70 %
	:alt: Paper create
	:align: center

If you fill the form and hit create, new entry will be created. In this case, you can choose any person
that has an entry in the database. If your database do not have an entry for the person you want to
attribute the paper to, you have to create a person for it. Details of how to create a person can be found
in other pages of this documentation.
