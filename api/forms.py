from django import forms

class TransactionUploadForm(forms.Form):
    file = forms.FileField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    text = forms.CharField(
        required=False, 
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Paste your transaction data here...'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get("file")
        text = cleaned_data.get("text")

        if not file and not text:
            raise forms.ValidationError("Please upload a file or paste text.")

        return cleaned_data

