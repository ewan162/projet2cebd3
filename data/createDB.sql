create table Departements (
    code_departement TEXT,
    nom_departement TEXT,
    code_region INTEGER,
    zone_climatique TEXT,
    constraint pk_departements primary key (code_departement),
    constraint fk_region foreign key (code_region) references Regions(code_region)
);

create table Regions (
    code_region INTEGER,
    nom_region TEXT,
    constraint pk_regions primary key (code_region)
);

create table Mesures (
    code_departement TEXT,
    date_mesure DATE,
    temperature_min_mesure FLOAT,
    temperature_max_mesure FLOAT,
    temperature_moy_mesure FLOAT,
    constraint pk_mesures primary key (code_departement, date_mesure),
    constraint fk_mesures foreign key (code_departement) references Departements(code_departement)
);

--TODO Q4 Ajouter les créations des nouvelles tables


create table Travaux (
    id_travaux INTEGER PRIMARY KEY AUTOINCREMENT,
    cout_total_travaux FLOAT,
    cout_induit_ht_Travaux FLOAT,
    annee_travaux INT,
    type_logement_Travaux TEXT,
    annee_construction_logement_Travaux INT,
    code_departement TEXT,
    type_travaux TEXT,
    CONSTRAINT fk_code_departement FOREIGN KEY (code_departement) REFERENCES Departements(code_departement),
    CONSTRAINT ck_type_travaux CHECK (type_travaux IN ('Isolation', 'Chauffage', 'Photovoltaique'))
);

create table Isolation (  
    poste_isolation TEXT,
    isolant_isolation TEXT,
    epaisseur_isolation INT,
    surface_isolation FLOAT,
    CONSTRAINT ck_type_poste CHECK (poste_isolation IN ('COMBLES PERDUES', 'ITI', 'ITE', 'RAMPANTS', 'SARKING', 'TOITURE TERASSE', 'SARKING', 'TOITURE TERRASSE', 'PLANCHER BAS'))
    -- CONSTRAINT ck_type_isolant CHECK (isolant_isolation IN ('AUTRES', 'LAINE VEGETALE', 'LAINE MINERALE', 'PLASTIQUES'))
);

create table Chauffage (
    energie_avant_travaux_chauffage TEXT,
    energie_installee_chauffage TEXT,
    generateur_chauffage  TEXT,
    type_chaudiere_chauffage  TEXT,
    -- CONSTRAINT ck_type_energie CHECK (energie_avant_travaux_chauffage IN ('AUTRES', 'BOIS', 'ELECTRICITE', 'FIOUL', 'GAZ') AND energie_installee_chauffage IN ('AUTRES', 'BOIS', 'ELECTRICITE', 'FIOUL', 'GAZ')),
    -- CONSTRAINT ck_type_generateur CHECK (generateur_chauffage IN ('AUTRES', 'CHAUDIERE', 'INSERT', 'PAC', 'POELE', 'RADIATEUR')),
    CONSTRAINT ck_type_chaudiere CHECK (type_chaudiere_chauffage IN ('STANDARD', 'AIR-EAU', 'A CONDENSATION', 'AUTRES', 'AIR-AIR', 'GEOTHERMIE', 'HPE'))
    -- id_travaux INT,
    -- CONSTRAINT fk_id_travaux FOREIGN KEY (id_travaux) REFERENCES Travaux(id_travaux)
);

create table Photovoltaique (
    puissance_installee_Photovoltaique INT,
    type_panneaux_Photovoltaique TEXT,
    CONSTRAINT ck_type_panneaux CHECK (type_panneaux_Photovoltaique IN ('MONOCRISTALLIN', 'POLYCRISTALLIN'))
    -- id_travaux INT NOT NULL,
    -- CONSTRAINT fk_id_travaux FOREIGN KEY (id_travaux) REFERENCES Travaux(id_travaux)

);


