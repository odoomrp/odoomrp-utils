Product packaging number
========================

* This module shows the "Packaging number" on objects "Stock move" and
  "Stock quant", for products that have an attribute of type "Package".
* To know if an attribute is of type "Package", the new check "Is Package" is
  created in "Product Attributes".
* The value of the new field "Packaging number", will be the result of
  multiplying the amount defined in the objects "Stock move" or "Stock quant",
  by the value of attribute "Package" defined in the product.
