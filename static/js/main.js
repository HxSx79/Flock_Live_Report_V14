// Add this at the beginning of the file
function showPartDetectionPopup(partInfo) {
    // Remove any existing popup
    const existingPopup = document.querySelector('.popup-notification');
    if (existingPopup) {
        existingPopup.remove();
    }

    // Create new popup
    const popup = document.createElement('div');
    popup.className = 'popup-notification';
    popup.innerHTML = `
        <h4>Part Detected</h4>
        <p><strong>Class:</strong> ${partInfo.class_name || 'N/A'}</p>
        <p><strong>Part Number:</strong> ${partInfo.part_number || 'N/A'}</p>
        <p><strong>Description:</strong> ${partInfo.description || 'N/A'}</p>
    `;

    // Add to document
    document.body.appendChild(popup);

    // Remove popup after animation
    setTimeout(() => {
        popup.remove();
    }, 3000);
}

// Modify the existing updateProductionData function
function updateProductionData() {
    fetch('/production_data')
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                console.error('Error in production data:', data.error);
                return;
            }

            // Check for new parts on Line 1
            const line1Delta = parseInt(data.line1_production.delta);
            if (line1Delta > 0) {
                showPartDetectionPopup({
                    class_name: 'Line 1',
                    part_number: data.line1_part.number,
                    description: data.line1_part.description
                });
            }

            // Check for new parts on Line 2
            const line2Delta = parseInt(data.line2_production.delta);
            if (line2Delta > 0) {
                showPartDetectionPopup({
                    class_name: 'Line 2',
                    part_number: data.line2_part.number,
                    description: data.line2_part.description
                });
            }

            // Update Line 1
            updateElement('program-1', data.line1_part.program);
            updateElement('part-number-1', data.line1_part.number);
            updateElement('part-description-1', data.line1_part.description);
            updateElement('quantity-1', data.line1_production.quantity);
            updateElement('delta-1', data.line1_production.delta);
            updateElement('scrap-1', data.line1_scrap.total);
            updateElement('scrap-rate-1', data.line1_scrap.rate + '%');

            // Update Line 2
            updateElement('program-2', data.line2_part.program);
            updateElement('part-number-2', data.line2_part.number);
            updateElement('part-description-2', data.line2_part.description);
            updateElement('quantity-2', data.line2_production.quantity);
            updateElement('delta-2', data.line2_production.delta);
            updateElement('scrap-2', data.line2_scrap.total);
            updateElement('scrap-rate-2', data.line2_scrap.rate + '%');

            // Update Totals
            updateElement('total-quantity', data.total_quantity);
            updateElement('total-delta', data.total_delta);
            updateElement('total-scrap', data.total_scrap);
            updateElement('average-scrap-rate', data.average_scrap_rate + '%');
            updateElement('last-refresh', data.current_time);
        })
        .catch(error => {
            console.error('Error updating production data:', error);
        });
}