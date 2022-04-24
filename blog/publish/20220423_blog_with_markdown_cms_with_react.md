# Using react to create a Blog and Portfolio with Markdown files as a CMS

I was always looking for an open-source solution to a web blog that uses Markdown files in a simple folder structure as a [CMS](https://en.wikipedia.org/wiki/Content_management_system). In the past, I often had to work with different kinds of CMS (Typo3, Joomla, WordPress, ...) and even develop websites using them. Those Systems all have their role, but I wanted something as simple as possible.

## Goal

So to summarize the goal:

```
Editor --> Markdown files --> Folder --> Backend --> Frontend --> Viewer
```

## Tools

### Frontend

I'm far off from being a frontend developer, but I've had some experiences with Angular and VueJS in the past. I always wanted to give React a try too, so this project seemed ideal for this.

The frontend would serve things like:

* Start
* About
* **Blog - Overview**
* **Blog - Posts**

#### Components

* **React**: Base JavaScript library
* **Parcel**: Web application bundler and build tool
* **Babel**: Code transpiler
* **Bootstrap**: CSS framework (for basic components and responsive behavior)
* **Moment**: Parse date strings
* **react-markdown**: Parse markdown string to HTML
* **react-icons**: Show Icons such as mail, LinkedIn, ...
* ... and a few more

### Backend

As for the backend component: I wanted something quick that would cost me as little time as possible to set up, so I chose python. I could always replace the backend if needed but something simple in python would work for now.

The backend would only serve an HTTP-REST API and communicate via JSON. It would read all markdown files from a folder and put them in a JSON array.

To get some metadata, the file name must be: ***YYYYMMMDD_title.md***. The date in the file name is then interpreted as the blog entry date.

#### Components

* **Flask**: web framework to provide endpoints:
  * **GET:posts/** : Get all posts
  * **GET:posts/<title>**: Get post by title
* **Waitress**: WSGI server

## Result

You can view the result here: <https://github.com/simongavris/portfolio-blog>.

## Conclusion

I love the idea of writing things in markdown and then having them published with few clicks. The process really motivates me on writing down more things for myself.

The project is far from finished. At most, it's a proof of concept. But at this stage, I realized that I really dislike the complexity of all the tools, frameworks, and components for what I require them to do. A simple page like this shouldn't rely on so many dependencies.

With all the learnings from this project, I want to start something new: An application that generates all web files in the backend and serves them as purely static files (no javascript). Let's see how this goes.

All in all, this was a fun project and I learned a lot about React, packaging webpages, and refreshed some Nginx knowledge.