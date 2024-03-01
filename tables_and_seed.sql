CREATE TABLE IF NOT EXISTS clientes (
    "id"                      SERIAL PRIMARY KEY,
    "limite"                  INT NOT NULL,
    "saldo_inicial"           INT DEFAULT 0 
);


CREATE TABLE IF NOT EXISTS transacoes (
    "id"             SERIAL PRIMARY KEY,
    "valor"          INT NOT NULL,
    "tipo"           VARCHAR(1) NOT NULL,
    "descricao"      VARCHAR(10) NOT NULL,
    "realizada_em"   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    "cliente_id"    INT NOT NULL,

    CONSTRAINT "clientes_fk" FOREIGN KEY ("cliente_id") REFERENCES clientes("id")
    
);


DO $$
BEGIN
  INSERT INTO clientes ("limite")
  VALUES
    (100000),
    (80000),
    (1000000),
    (10000000),
    (500000);
END; $$