# Data Dictionary

### Deck

- deck_id (pk)
- name
- private

### Deck_User

- deck_id (pk)
- user_id (pk)
- role_cd

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
- status_cd
- date_to_review
