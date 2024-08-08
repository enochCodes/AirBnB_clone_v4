$(function() {
	const selectedAmenities = {};

	$('input[type="checkbox"]').change(function () {
		const amenityId = $(this).attr('data-id');
		const amenityName = $(this).attr('data-name');

		if (this.checked) {
			selectedAmenities[amenityId] = amenityName;
		} else {
			delete selectedAmenities[amenityId];
		}

		const amenityList = object.values(selectedAmenities).join(', ');
		if (amenityList.length > 0) {
			$('.filters h4').text('Amenities: ${amenityList}');
		} else {
			$('.filters h4').html('&nbsp;');
		}
	});
});
