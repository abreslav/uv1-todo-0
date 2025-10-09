


Todoer is a a personal ToDo app.

### Tech Stack
- Django
- Tailwind CSS

### Data

- Todo list item
  - content: plain text
  - created_at
  - marked_as_done_at

### Users and permissions

- users can sign in with Google (no email/password sign in)
- every user sees only their own todo items

### User stories

- add a new entry
  - support Markdown
    - in the edit box, raw Markdown is displayed (no WYSIWYG)
    - when saved, rendered Markdown is displayed
- mark entry as Done (checkbox)
- remove an entry

### Non-functional requirements

- Markdown is rendered on the client side using marked.js