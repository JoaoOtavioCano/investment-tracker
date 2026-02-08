
CREATE DATABASE investmenttracker;


ALTER DATABASE investmenttracker OWNER TO postgres;

\connect investmenttracker


SET default_tablespace = '';

SET default_table_access_method = heap;


CREATE TABLE public.assets (
    userid integer NOT NULL,
    name character varying(30) NOT NULL,
    type character varying(30) NOT NULL
);


ALTER TABLE public.assets OWNER TO postgres;



CREATE TABLE public.newpasswordsrequests (
    code character varying(100) NOT NULL,
    userid integer NOT NULL
);


ALTER TABLE public.newpasswordsrequests OWNER TO postgres;


CREATE TABLE public.stocks (
    userid integer NOT NULL,
    name character varying(30) NOT NULL,
    quantity double precision NOT NULL,
    cost double precision NOT NULL,
    country character varying(2) DEFAULT 'US'::character varying NOT NULL
);


ALTER TABLE public.stocks OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16397)
-- Name: transactions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transactions (
    userid integer NOT NULL,
    id integer NOT NULL,
    date_time date NOT NULL,
    asset character varying(30) NOT NULL,
    quantity double precision NOT NULL,
    cost double precision NOT NULL,
    operation character varying(30) NOT NULL,
    current_avg_cost double precision,
    type text NOT NULL
);


ALTER TABLE public.transactions OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16396)
-- Name: transactions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.transactions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.transactions_id_seq OWNER TO postgres;

--
-- TOC entry 3398 (class 0 OID 0)
-- Dependencies: 217
-- Name: transactions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.transactions_id_seq OWNED BY public.transactions.id;


--
-- TOC entry 216 (class 1259 OID 16390)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    userid integer NOT NULL,
    email character varying(100) NOT NULL,
    password character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16389)
-- Name: users_userid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_userid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_userid_seq OWNER TO postgres;

--
-- TOC entry 3399 (class 0 OID 0)
-- Dependencies: 215
-- Name: users_userid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_userid_seq OWNED BY public.users.userid;


--
-- TOC entry 3221 (class 2604 OID 16400)
-- Name: transactions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions ALTER COLUMN id SET DEFAULT nextval('public.transactions_id_seq'::regclass);


--
-- TOC entry 3220 (class 2604 OID 16393)
-- Name: users userid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN userid SET DEFAULT nextval('public.users_userid_seq'::regclass);



ALTER TABLE ONLY public.assets
    ADD CONSTRAINT assets_pkey PRIMARY KEY (userid, name);


--
-- TOC entry 3230 (class 2606 OID 16412)
-- Name: newpasswordsrequests newpasswordsrequests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.newpasswordsrequests
    ADD CONSTRAINT newpasswordsrequests_pkey PRIMARY KEY (userid);


--
-- TOC entry 3224 (class 2606 OID 16451)
-- Name: users second_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT second_key UNIQUE (email);


--
-- TOC entry 3236 (class 2606 OID 16430)
-- Name: stocks stocks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stocks
    ADD CONSTRAINT stocks_pkey PRIMARY KEY (userid, name);


--
-- TOC entry 3228 (class 2606 OID 16402)
-- Name: transactions transactions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT transactions_pkey PRIMARY KEY (id);


--
-- TOC entry 3232 (class 2606 OID 16414)
-- Name: newpasswordsrequests uq_newpasswordsrequests_userid; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.newpasswordsrequests
    ADD CONSTRAINT uq_newpasswordsrequests_userid UNIQUE (code);


--
-- TOC entry 3226 (class 2606 OID 16395)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (userid);


--
-- TOC entry 3240 (class 2606 OID 16431)
-- Name: stocks fk; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.stocks
    ADD CONSTRAINT fk FOREIGN KEY (userid, name) REFERENCES public.assets(userid, name) ON DELETE CASCADE;


--
-- TOC entry 3239 (class 2606 OID 16441)
-- Name: assets fk_assets_userid; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.assets
    ADD CONSTRAINT fk_assets_userid FOREIGN KEY (userid) REFERENCES public.users(userid) ON DELETE CASCADE;


--
-- TOC entry 3238 (class 2606 OID 16436)
-- Name: newpasswordsrequests fk_newpasswordsrequests_userid; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.newpasswordsrequests
    ADD CONSTRAINT fk_newpasswordsrequests_userid FOREIGN KEY (userid) REFERENCES public.users(userid) ON DELETE CASCADE;


--
-- TOC entry 3237 (class 2606 OID 16403)
-- Name: transactions fk_userid; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transactions
    ADD CONSTRAINT fk_userid FOREIGN KEY (userid) REFERENCES public.users(userid) ON DELETE CASCADE;


-- Completed on 2026-02-08 14:49:00 -03

--
-- PostgreSQL database dump complete
--

