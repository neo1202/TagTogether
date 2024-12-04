CREATE TABLE "users" (
  "id" SERIAL PRIMARY KEY,
  "username" VARCHAR UNIQUE,
  "password" VARCHAR,
  "is_old_customer" BOOLEAN DEFAULT FALSE,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "teams" (
  "id" SERIAL PRIMARY KEY,
  "name" VARCHAR UNIQUE,
  "created_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "team_members" (
  "id" SERIAL PRIMARY KEY,
  "team_id" INTEGER,
  "user_id" INTEGER,
  "weight" FLOAT,
  "joined_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "checkins" (
  "id" SERIAL PRIMARY KEY,
  "team_id" INTEGER,
  "user_id" INTEGER,
  "timestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  "post_url" VARCHAR,
  "is_new_user" BOOLEAN DEFAULT FALSE
);

CREATE TABLE "scores" (
  "id" SERIAL PRIMARY KEY,
  "team_id" INTEGER,
  "score" FLOAT,
  "updated_at" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON COLUMN "users"."username" IS 'User''s unique username';
COMMENT ON COLUMN "users"."password" IS 'Plain text password';
COMMENT ON COLUMN "users"."is_old_customer" IS 'Indicates if the user is a returning customer';
COMMENT ON COLUMN "users"."created_at" IS 'User creation time';

COMMENT ON COLUMN "teams"."name" IS 'Team name';
COMMENT ON COLUMN "teams"."created_at" IS 'Team creation time';

COMMENT ON COLUMN "team_members"."team_id" IS 'Reference to team';
COMMENT ON COLUMN "team_members"."user_id" IS 'Reference to user';
COMMENT ON COLUMN "team_members"."weight" IS 'User''s weight in the team';
COMMENT ON COLUMN "team_members"."joined_at" IS 'Time the user joined the team';

COMMENT ON COLUMN "checkins"."team_id" IS 'Reference to team';
COMMENT ON COLUMN "checkins"."user_id" IS 'Reference to user';
COMMENT ON COLUMN "checkins"."timestamp" IS 'Check-in timestamp';
COMMENT ON COLUMN "checkins"."post_url" IS 'URL of the associated social media post';
COMMENT ON COLUMN "checkins"."is_new_user" IS 'Indicator if user is new';

COMMENT ON COLUMN "scores"."team_id" IS 'Reference to team';
COMMENT ON COLUMN "scores"."score" IS 'Calculated score for the team';
COMMENT ON COLUMN "scores"."updated_at" IS 'Last updated time';

ALTER TABLE "team_members" ADD FOREIGN KEY ("team_id") REFERENCES "teams" ("id");
ALTER TABLE "team_members" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");
ALTER TABLE "checkins" ADD FOREIGN KEY ("team_id") REFERENCES "teams" ("id");
ALTER TABLE "checkins" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");
ALTER TABLE "scores" ADD FOREIGN KEY ("team_id") REFERENCES "teams" ("id");
