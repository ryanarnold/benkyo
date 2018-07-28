# Data Dictionary

### Deck

- deck_id (pk)
- name
- visibility

### Deck_User

- deck_id (pk)
- user_id (pk)
- role_cd

### User_Role

- role_cd (pk)

### Card

- card_id (pk)
- deck_id
- front
- back

### Card_Tags

- card_id (pk)
- tag (pk)

### Review

- card_id (pk)
- user_id (pk)
- status_id
- date_to_review

### Status

- status_id (pk)
- days_before_review