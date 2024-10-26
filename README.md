# RateMyBoilerHousing.com

Site to rate housing around Purdue University


## Database Design

```
User(user_id, name, email)
Housing(housing_id, address)
RoomType(roomtype_id, friendly_name)
Offering(offering_id, housing_id, roomtype_id, cost)
Review(review_id, offering_id, stars, review_desc)
```