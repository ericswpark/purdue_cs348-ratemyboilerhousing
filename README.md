# RateMyBoilerHousing.com

Site to rate housing around Purdue University


## Database Design

Underlined text is primary key (PK), bolded text is foreign key (FK)

---

User(<u>user_id</u>, name, email)

Housing(<u>housing_id</u>, name, address)

RoomType(<u>roomtype_id</u>, friendly_name, bedroom_count, bathroom_count)

Offering(<u>offering_id</u>, **housing_id**, **roomtype_id**, cost)

Review(<u>review_id</u>, **offering_id**, **user_id**, stars, review_desc)
