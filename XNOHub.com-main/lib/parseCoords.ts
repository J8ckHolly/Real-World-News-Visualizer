export function formatLatitude(latitude: number): string {
    // Round the latitude to 3 decimal places
    const roundedLatitude = Math.abs(latitude).toFixed(3);
    
    // Check if the latitude is positive or negative and append N or S
    if (latitude >= 0) {
        return `${roundedLatitude} °N`;  // Positive latitude gets N
    } else {
        return `${roundedLatitude} °S`;  // Negative latitude gets S
    }
}


export function formatLongitude(longitude: number): string {
    // Round the longitude to 3 decimal places
    const roundedLongitude = Math.abs(longitude).toFixed(3);
    
    // Check if the longitude is positive or negative and append E or W with the degree symbol
    if (longitude >= 0) {
        return `${roundedLongitude} °E`;  // Positive longitude gets E
    } else {
        return `${roundedLongitude} °W`;  // Negative longitude gets W
    }
}
