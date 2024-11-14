from django import forms

from .models import BoardingHouse, BoardingRoom, Tag, BoardingHouseImage, BoardingRoomImage, BoardingRoomTag
from features.address.models import Barangay, Municipality


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleImageField(forms.ImageField):
    def __init__(self, *args, max_images=5, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        self.max_images = max_images
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            if len(data) > self.max_images:
                raise forms.ValidationError(f"You can upload a maximum of {self.max_images} images.")
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class CreateBoardingHouseForm(forms.ModelForm):
    form_name = 'create_boarding_house_form'
    prefix = 'create_boarding_house_form'
    images = MultipleImageField(required=False, max_images=5)

    class Meta:
        model = BoardingHouse
        fields = '__all__'
        exclude = ['created_at', 'updated_at', 'landlord']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['province'].empty_label = "Select a province"
        self.fields['municipality'].queryset = Municipality.objects.none()
        self.fields['municipality'].empty_label = "Select a municipality"
        self.fields['barangay'].queryset = Barangay.objects.none()
        self.fields['barangay'].empty_label = "Select a barangay"

        province_html_name = self.add_prefix('province')
        municipality_html_name = self.add_prefix('municipality')

        if province_html_name in self.data:
            try:
                province_id = int(self.data.get(province_html_name))
                self.fields['municipality'].queryset = Municipality.objects.filter(province_id=province_id).order_by(
                    'name')
            except (ValueError, TypeError):
                pass

        if municipality_html_name in self.data:
            try:
                municipality_id = int(self.data.get(municipality_html_name))
                self.fields['barangay'].queryset = Barangay.objects.filter(municipality_id=municipality_id).order_by(
                    'name')
            except (ValueError, TypeError):
                pass

        elif self.instance.pk:
            self.fields['municipality'].queryset = self.instance.province.municipality_set.order_by('name')
            self.fields['barangay'].queryset = self.instance.municipality.barangay_set.order_by('name')

    def save(self, commit=True):
        boarding_house = super().save(commit=False)
        if commit:
            boarding_house.save()
            images = self.files.getlist('images')
            for image in images:
                BoardingHouseImage.objects.create(boarding_house=boarding_house, image=image)
        return boarding_house


class CreateBoardingRoomForm(forms.ModelForm):
    form_name = 'create_boarding_room_form'
    prefix = 'create_boarding_room_form'
    images = MultipleImageField(required=False, max_images=5)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.filter(type=Tag.Type.BOARDING_ROOM),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    quantity = forms.IntegerField(min_value=1, max_value=5, initial=1)

    class Meta:
        model = BoardingRoom
        fields = '__all__'
        exclude = ['created_at', 'updated_at', 'is_available']

    def __init__(self, landlord, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['boarding_house'].queryset = BoardingHouse.objects.filter(landlord=landlord)
        self.fields['boarding_house'].empty_label = "Select a boarding house"

    def save(self, commit=True):
        quantity = self.cleaned_data.get('quantity', 1)
        boarding_rooms = []
        for _ in range(quantity):
            boarding_room = super().save(commit=False)
            boarding_room.pk = None  # By setting the primary key to None, a new object will be saved each time.
            if commit:
                boarding_room.save()
                images = self.files.getlist('images')
                for image in images:
                    BoardingRoomImage.objects.create(boarding_room=boarding_room, image=image)
                tags = self.cleaned_data.get('tags')
                for tag in tags:
                    BoardingRoomTag.objects.create(boarding_room=boarding_room, tag=tag)
            boarding_rooms.append(boarding_room)
        return boarding_rooms