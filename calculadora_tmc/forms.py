from django import forms


class TmcForm(forms.Form):
    credit_amount = forms.DecimalField(label='Monto del crédito en UF', required=True)
    time_to_maturity = forms.DecimalField(label='Plazo del crédito en días', required=True)
    query_date = forms.DateField(label='Fecha a consultar por TMC (YYYY-MM-DD)', required=True)
    credit_types = [("Operaciones no reajustables", "No reajustable "), ("Operaciones reajustables", "Reajustable"), ("Operaciones expresadas en moneda extranjera", "Moneda extranjera")]
    credit_type = forms.ChoiceField(choices=credit_types, label="Tipo de crédito")
