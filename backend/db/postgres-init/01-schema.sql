CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "user_name" VARCHAR UNIQUE,
  "password" VARCHAR,
  "weight" FLOAT DEFAULT 1,
  "is_old_customer" BOOLEAN DEFAULT FALSE,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "teams" (
  "id" SERIAL PRIMARY KEY,
  "team_name" VARCHAR UNIQUE,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "team_members" (
  "id" SERIAL PRIMARY KEY,
  "team_id" INTEGER,
  "user_id" INTEGER,
  "team_name" VARCHAR,
  "user_name" VARCHAR,
  "joined_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "checkins" (
  "id" SERIAL PRIMARY KEY,
  "team_id" INTEGER,
  "user_id" INTEGER,
  "team_name" VARCHAR,
  "user_name" VARCHAR,
  "timestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "post_url" VARCHAR
);

CREATE TABLE "scores" (
  "id" SERIAL PRIMARY KEY,
  "team_id" INTEGER,
  "team_name" VARCHAR,
  "score" FLOAT,
  "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE "team_members" ADD FOREIGN KEY ("team_id") REFERENCES "teams" ("id");
ALTER TABLE "team_members" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");
ALTER TABLE "checkins" ADD FOREIGN KEY ("team_id") REFERENCES "teams" ("id");
ALTER TABLE "checkins" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");
ALTER TABLE "scores" ADD FOREIGN KEY ("team_id") REFERENCES "teams" ("id");
