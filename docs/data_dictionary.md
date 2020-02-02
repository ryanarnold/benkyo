Table Deck {
  deck_id int [pk]
  name varchar
  private boolean
}

Table User {
  user_id int [pk]
  email varchar
  username varchar
}

Table DeckUser {
  id int [pk]
  deck int [ref: > Deck.deck_id, unique]
  user int [ref: > User.user_id, unique]
  role_cd varchar [unique]
}

Table Card {
   card_id int [pk]
   deck int [ref: > Deck.deck_id]
   front varchar
   back varchar
}

Table CardTag {
  card int [ref: > Card.card_id]
  tag varchar
}

Table Review {
  card int [ref: > Card.card_id]
  user int [ref: > User.user_id]
  status_cd varchar
  date_to_review date
}