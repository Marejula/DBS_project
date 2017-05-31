


CREATE TABLE HASHTAG(
hashtag_name          VARCHAR(50) NOT NULL,
CONSTRAINT Hashtag_pkey PRIMARY KEY (hashtag_name));

CREATE TABLE TWEET(
t_ID                      INTEGER NOT NULL,
handle                    VARCHAR(30) NOT NULL,
t_text                    VARCHAR(200),
is_retweet                BOOLEAN,
original_author           VARCHAR(50),
t_time                    TIMESTAMP NOT NULL,
in_reply_to_screen_name   VARCHAR(50),
is_quote_status           BOOLEAN,
retweet_count             INTEGER,
favorite_count            INTEGER,
CONSTRAINT Tweet_pkey PRIMARY KEY (t_ID));

CREATE TABLE ENTHAELT(
e_ID            INTEGER NOT NULL,
t_ID            INTEGER NOT NULL,
hashtag_name    VARCHAR(50) NOT NULL,
CONSTRAINT Enthaelt_pkey PRIMARY KEY (e_ID),
CONSTRAINT e_Hashtag_fkey FOREIGN KEY (hashtag_name)
                          REFERENCES HASHTAG(hashtag_name),
CONSTRAINT e_Tweet_fkey FOREIGN KEY (t_ID)
                        REFERENCES TWEET(t_ID));



