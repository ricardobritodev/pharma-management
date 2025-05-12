-- Insere produtos farmacêuticos de exemplo
INSERT INTO produtos (nome_produto, principio_ativo, lote, quantidade, preco, data_validade, fabricante, categoria) VALUES
-- Analgésicos
('Dipirona 500mg', 'Dipirona Sódica', 'LOT20230101', 150, 8.90, '2025-06-30', 'EMS', 'Analgésico'),
('Tylenol 750mg', 'Paracetamol', 'LOT20230215', 200, 15.50, '2024-12-31', 'Johnson & Johnson', 'Analgésico'),
('Ibuprofeno 400mg', 'Ibuprofeno', 'LOT20230322', 180, 12.75, '2025-03-15', 'Eurofarma', 'Anti-inflamatório'),

-- Antibióticos
('Amoxicilina 500mg', 'Amoxicilina Triidratada', 'LOT20230410', 90, 28.90, '2024-11-30', 'Novartis', 'Antibiótico'),
('Azitromicina 500mg', 'Azitromicina Diidratada', 'LOT20230505', 75, 45.00, '2025-01-20', 'Pfizer', 'Antibiótico'),

-- Anti-hipertensivos
('Losartana 50mg', 'Losartana Potássica', 'LOT20230618', 120, 22.30, '2026-05-15', 'Aché', 'Anti-hipertensivo'),
('Atenolol 25mg', 'Atenolol', 'LOT20230722', 110, 18.75, '2025-09-30', 'Sanofi', 'Anti-hipertensivo'),

-- Diabetes
('Metformina 850mg', 'Cloridrato de Metformina', 'LOT20230830', 95, 14.90, '2025-07-31', 'Medley', 'Diabetes'),
('Glibenclamida 5mg', 'Glibenclamida', 'LOT20230912', 85, 19.50, '2024-10-15', 'Bayer', 'Diabetes'),

-- Produtos de higiene
('Álcool em Gel 70% 500ml', 'Etanol', 'LOT20231005', 60, 12.90, '2026-02-28', 'Dermachem', 'Higiene'),
('Sabonete Líquido Antibacteriano', 'Triclosan', 'LOT20231120', 45, 9.80, '2025-08-15', 'Johnson & Johnson', 'Higiene'),

-- Termolábeis (produtos que precisam de refrigeração)
('Vacina Influenza 2023', 'Vírus Influenza Inativado', 'LOT20231201', 30, 89.90, '2023-12-31', 'Butantan', 'Vacina'),
('Insulina NPH 100UI/ml', 'Insulina Humana', 'LOT20240115', 25, 120.00, '2024-06-30', 'Novo Nordisk', 'Diabetes'),

-- Fitoterápicos
('Chá de Camomila 20g', 'Matricaria chamomilla', 'LOT20240210', 50, 6.50, '2025-10-31', 'Herbarium', 'Fitoterápico'),
('Valeriana 500mg', 'Valeriana officinalis', 'LOT20240305', 40, 24.90, '2024-09-30', 'Nativa', 'Fitoterápico'),

-- Dermatológicos
('Hidratante Corporal 200ml', 'Ureia 10%', 'LOT20240418', 35, 32.50, '2025-11-30', 'Dermatus', 'Dermatológico'),
('Protetor Solar FPS 50', 'Avobenzona, Octocrileno', 'LOT20240522', 55, 58.90, '2024-12-31', 'La Roche-Posay', 'Dermatológico');

-- Visualiza os dados inseridos
SELECT * FROM produtos ORDER BY categoria, nome_produto;
