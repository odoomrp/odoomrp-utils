# -*- coding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'MRP Production Unreserve Movements',
    'version': "8.0.1.1.0",
    'author': 'OdooMRP team,'
              'AvanzOSC,'
              'Serv. Tecnol. Avanzados - Pedro M. Baeza',
    'website': "http://www.odoomrp.com",
    "contributors": [
        "Pedro M. Baeza <pedro.baeza@serviciosbaeza.com>",
        "Ana Juaristi <anajuaristi@avanzosc.es>",
        "Alfredo de la Fuente <alfredodelafuente@avanzosc.es>",
        "Ainara Galdona <ainaragaldona@avanzosc.es>"
        ],
    'category': 'Manufacturing',
    'depends': ['mrp',
                'mrp_operations',
                'mrp_operations_extension'
                ],
    'data': ["views/mrp_production_view.xml",
             "views/mrp_production_workcenter_line_view.xml",
             "views/mrp_production_workflow.xml"
             ],
    'installable': True,
}
