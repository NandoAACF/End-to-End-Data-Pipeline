function parse() {
    let inputString = window.APP_INITIALIZATION_STATE[3][6];
    let substringToRemove = ")]}'";

    let modifiedString;
    if (inputString.startsWith(substringToRemove)) {
        modifiedString = inputString.slice(substringToRemove.length);
    }
    return JSON.parse(modifiedString);
}

function get_rating(data) {
    return data?.[6]?.[4]?.[7];
}

function get_reviews(data) {
    return data?.[6]?.[4]?.[8];
}

function get_title(data) {
    return data?.[6]?.[11];
}

function get_more_data() {
    let data = parse();

    let rating = get_rating(data);
    let reviews = get_reviews(data);

    let title = get_title(data);

    return {
        title,
        rating,
        reviews,
    };
}

return get_more_data();
