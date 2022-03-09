--
-- PostgreSQL database dump
--

-- Dumped from database version 13.6
-- Dumped by pg_dump version 13.6

-- Started on 2022-03-09 20:44:22

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 200 (class 1259 OID 24869)
-- Name: movies; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.movies (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    categories character varying(50),
    release_year character varying(4),
    movie_rating real,
    star character varying(150)
);


ALTER TABLE public.movies OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 24872)
-- Name: movies_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.movies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movies_id_seq OWNER TO postgres;

--
-- TOC entry 3017 (class 0 OID 0)
-- Dependencies: 201
-- Name: movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.movies_id_seq OWNED BY public.movies.id;


--
-- TOC entry 202 (class 1259 OID 24874)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    first_name character varying(50) NOT NULL,
    email character varying(200),
    password character varying(600)
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 203 (class 1259 OID 24880)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 3018 (class 0 OID 0)
-- Dependencies: 203
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 204 (class 1259 OID 24882)
-- Name: watch; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.watch (
    id integer NOT NULL,
    movie_id integer NOT NULL,
    user_id integer NOT NULL,
    username character varying(50),
    rent_date date NOT NULL,
    return_date date
);


ALTER TABLE public.watch OWNER TO postgres;

--
-- TOC entry 205 (class 1259 OID 24885)
-- Name: watch_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.watch_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.watch_id_seq OWNER TO postgres;

--
-- TOC entry 3019 (class 0 OID 0)
-- Dependencies: 205
-- Name: watch_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.watch_id_seq OWNED BY public.watch.id;


--
-- TOC entry 2863 (class 2604 OID 24887)
-- Name: movies id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movies ALTER COLUMN id SET DEFAULT nextval('public.movies_id_seq'::regclass);


--
-- TOC entry 2864 (class 2604 OID 24888)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 2865 (class 2604 OID 24889)
-- Name: watch id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.watch ALTER COLUMN id SET DEFAULT nextval('public.watch_id_seq'::regclass);


--
-- TOC entry 3006 (class 0 OID 24869)
-- Dependencies: 200
-- Data for Name: movies; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.movies (id, name, categories, release_year, movie_rating, star) VALUES (1, 'Avatar', 'Sci-Fi,Action,Adventure,Fantasy', '2009', 7.8, 'Sam Worthington');
INSERT INTO public.movies (id, name, categories, release_year, movie_rating, star) VALUES (2, 'Avengers: Endgame', 'Action,Adventure,Sci-Fi', '2019', 8.4, 'Robert Downey Jr.');
INSERT INTO public.movies (id, name, categories, release_year, movie_rating, star) VALUES (3, 'Titanic', 'Drama,Romance', '1997', 7.8, 'Leonardo DiCaprio');
INSERT INTO public.movies (id, name, categories, release_year, movie_rating, star) VALUES (4, 'Star Wars: Episode VII - The Force Awakens', 'Animation,Action,Adventure,Drama,Fantasy,Sci-Fi', '2015', 7.8, 'Daisy Ridley');
INSERT INTO public.movies (id, name, categories, release_year, movie_rating, star) VALUES (5, 'Spider-Man: No Way Home', 'Sci-Fi,Action,Adventure,Fantasy', '2021', 8.7, 'Tom Holland');
INSERT INTO public.movies (id, name, categories, release_year, movie_rating, star) VALUES (6, 'Avengers: Infinity War', 'Action,Adventure,Sci-Fi', '2018', 8.4, 'Robert Downey Jr.');


--
-- TOC entry 3008 (class 0 OID 24874)
-- Dependencies: 202
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.users (id, first_name, email, password) VALUES (1, 'kostas', 'kostantinosmavros28@gmail.com', 'sha256$pXHDShUMnTvQU2fO$189f358d644aa84d9801860644461bda366d3d7b8c36e77e46c33d69d9b534fb');
INSERT INTO public.users (id, first_name, email, password) VALUES (6, 'kostas27', 'kostantinosmavros28@gmasfasfasail.com', 'sha256$Nebbi1xfnfTcG6Nu$91108cc315a74f0a8c5daff9f3c3c47f2ebbb87eaf38e96cadb910c934ba43dc');


--
-- TOC entry 3010 (class 0 OID 24882)
-- Dependencies: 204
-- Data for Name: watch; Type: TABLE DATA; Schema: public; Owner: postgres
--

INSERT INTO public.watch (id, movie_id, user_id, username, rent_date, return_date) VALUES (1, 1, 1, 'kostas', '2022-02-28', '2022-02-28');
INSERT INTO public.watch (id, movie_id, user_id, username, rent_date, return_date) VALUES (2, 2, 1, 'kostas', '2022-03-04', '2022-03-04');
INSERT INTO public.watch (id, movie_id, user_id, username, rent_date, return_date) VALUES (3, 3, 1, 'kostas', '2022-03-05', '2022-03-05');
INSERT INTO public.watch (id, movie_id, user_id, username, rent_date, return_date) VALUES (5, 4, 1, 'kostas', '2022-03-09', NULL);
INSERT INTO public.watch (id, movie_id, user_id, username, rent_date, return_date) VALUES (4, 5, 1, 'kostas', '2022-03-09', '2022-03-09');


--
-- TOC entry 3020 (class 0 OID 0)
-- Dependencies: 201
-- Name: movies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.movies_id_seq', 1, false);


--
-- TOC entry 3021 (class 0 OID 0)
-- Dependencies: 203
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 6, true);


--
-- TOC entry 3022 (class 0 OID 0)
-- Dependencies: 205
-- Name: watch_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.watch_id_seq', 5, true);


--
-- TOC entry 2867 (class 2606 OID 24891)
-- Name: movies movie_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movie_name UNIQUE (name) INCLUDE (name);


--
-- TOC entry 2869 (class 2606 OID 24893)
-- Name: movies movies_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id, name);


--
-- TOC entry 2871 (class 2606 OID 24895)
-- Name: users users_name; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_name UNIQUE (first_name) INCLUDE (first_name);


--
-- TOC entry 2873 (class 2606 OID 24897)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 2875 (class 2606 OID 24899)
-- Name: watch watch_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.watch
    ADD CONSTRAINT watch_pkey PRIMARY KEY (id);


-- Completed on 2022-03-09 20:44:22

--
-- PostgreSQL database dump complete
--

