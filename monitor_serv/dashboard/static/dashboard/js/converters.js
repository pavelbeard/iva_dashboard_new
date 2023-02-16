export function convertBytesToMetric(amountStr) {
    let amount = parseInt(amountStr);

    if (amount >= 0 && amount < 1000) {
        return `${amount}B`;
    }
    else if (amount >= 1000 && amount < 1_000_000) {
        return `${(amount / 1000).toFixed(2)}KB`;
    }
    else if (amount >= 1_000_000 && amount < 1_000_000_000) {
        return `${(amount / 1000 ** 2).toFixed(2)}MB`;
    }
    else if (amount >= 1_000_000_000 && amount < 1_000_000_000_000){
        return `${(amount / 1000 ** 3).toFixed(2)}GB`;
    } else {
        return `${(amount / 1000 ** 4).toFixed(2)}TB`;
    }
}