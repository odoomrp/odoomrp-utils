account invoice line stock move info
====================================
This module informs to the invoice line, the movement of stock that
corresponds.

For having this field correctly filled, you have to uncheck "Group Invoice
Lines" option in the sale and purchase journals.

When an invoice is canceled, it offers picking as "To be invoiced". If an
invoice is deleted, It validates that the picking is in the status "Cancelled".

In version 9 of "stock_account" module you have already introduced the new
"move_id" field, so this module is not necessary, and we will have to modify
the "stock.account" module to put him treat invoices.

Credits
=======

Contributors
------------
* Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>
* Ana Juaristi <anajuaristi@avanzosc.es>
* Alfredo de la Fuente <alfredodelafuente@avanzosc.es>
* Unai Alkorta <practicas@avanzosc.es>
* Iñaki Zabala <practicas@avanzosc.es>
