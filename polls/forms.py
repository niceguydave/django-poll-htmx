from django import forms


class SearchForm(forms.Form):
    search_text = forms.CharField(max_length=20, required=True)

    # Predefined list of blocked words
    BLOCKED_WORDS = ["🫤", "spam"]

    def clean_search_text(self):
        search_text = self.cleaned_data["search_text"].lower()
        for word in self.BLOCKED_WORDS:
            if word in search_text:
                raise forms.ValidationError(f"Dude, don't say '{word}'.")
        return search_text
