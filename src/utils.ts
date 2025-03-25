function randomString(length: number) {
    let result = '';
    const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    const charactersLength = characters.length;
    let counter = 0;
    while (counter < length) {
        result += characters.charAt(Math.floor(Math.random() * charactersLength));
        counter += 1;
    }
    return result;
}

export function generateFileNameForUser(fileName: string) {
    const date = new Date();
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hour = String(date.getHours()).padStart(2, '0');
    const min = String(date.getMinutes()).padStart(2, '0');
    const sec = String(date.getSeconds()).padStart(2, '0');

    const randomPrefix = randomString(6);
    const name = fileName.replace(/ /g, '+');
    const formattedDate = `${day}${month}${year}_${hour}${min}${sec}`;
    return `${randomPrefix}-${formattedDate}-${name}`;
}

export function timeSince(date: string) {
    const now_date = new Date();
    var now_utc = new Date(Date.UTC(now_date.getUTCFullYear(), now_date.getUTCMonth(),
        now_date.getUTCDate(), now_date.getUTCHours(),
        now_date.getUTCMinutes(), now_date.getUTCSeconds()));

    const current_date_utc = new Date(date).getTime();
    const seconds = Math.floor((now_utc.getTime() - current_date_utc) / 1000);
    let interval = seconds / 31536000;
    if (isNaN(interval)) {
        return "---";
    }
    if (interval > 1) {
        return Math.floor(interval) + " year" + (interval < 2 ? "" : "s ago");
    }
    interval = seconds / 2592000;
    if (interval > 1) {
        return Math.floor(interval) + " month" + (interval < 2 ? "" : "s ago");
    }
    interval = seconds / 86400;
    if (interval > 1) {
        return Math.floor(interval) + " day" + (interval < 2 ? "" : "s ago");
    }
    interval = seconds / 3600;
    if (interval > 1) {
        return Math.floor(interval) + " hour" + (interval < 2 ? "" : "s ago");
    }
    interval = seconds / 60;
    if (interval > 1) {
        return Math.floor(interval) + " minute" + (interval < 2 ? "" : "s ago");
    }
    return Math.floor(seconds) + " second" + (seconds < 2 ? "" : "s ago");
}
