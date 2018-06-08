/*
[BP-MM] Reverso masivo de facturas de clientes en estado "pagadas"
08/06/2018
*/

--294;"Cuentas por Cobrar a Clientes"
--select * from account_account where company_id = 3 and name ilike '%cobrar%'

--48
/*
select * from account_invoice ai
inner join account_move am on ai.move_id = am.id
inner join account_move_line aml on am.id = aml.move_id
where 
aml.name = ai.name
and ai.id in (
137,
134,
136,
135,
130,
127,
123,
125,
119,
120,
186,
180,
164,
163,
158,
155,
150,
152,
148,
117,
115,
114,
113,
112,
108,
107,
106,
105,
101,
99,
96,
97,
93,
87,
78,
79,
68,
6,
21,
10,
28,
27,
8,
12,
18,
15,
20,
13
)

*/


--UPADATE aml
update account_move_line set account_id = 294, debit_cash_basis = 0.00, balance_cash_basis = 0.00, amount_residual = tlb.balance
from (
select ai.id as ai_id, am.id as am_id, aml.id as aml_id, aml.balance from account_invoice ai
inner join account_move am on ai.move_id = am.id
inner join account_move_line aml on am.id = aml.move_id
where 
aml.name = ai.name
and ai.id in (
137,
134,
136,
135,
130,
127,
123,
125,
119,
120,
186,
180,
164,
163,
158,
155,
150,
152,
148,
117,
115,
114,
113,
112,
108,
107,
106,
105,
101,
99,
96,
97,
93,
87,
78,
79,
68,
6,
21,
10,
28,
27,
8,
12,
18,
15,
20,
13
)
) tlb
where tlb.aml_id = account_move_line.id;


--UPDATE ai
update account_invoice set state = 'open', account_id = 294, 
residual = tlb.balance, residual_signed = tlb.balance, residual_company_signed = tlb.balance,
reconciled = False
from (
select ai.id as ai_id, am.id as am_id, aml.id as aml_id, aml.balance from account_invoice ai
inner join account_move am on ai.move_id = am.id
inner join account_move_line aml on am.id = aml.move_id
where 
aml.name = ai.name
and ai.id in (
137,
134,
136,
135,
130,
127,
123,
125,
119,
120,
186,
180,
164,
163,
158,
155,
150,
152,
148,
117,
115,
114,
113,
112,
108,
107,
106,
105,
101,
99,
96,
97,
93,
87,
78,
79,
68,
6,
21,
10,
28,
27,
8,
12,
18,
15,
20,
13
)
) tlb
where tlb.ai_id = account_invoice.id;
