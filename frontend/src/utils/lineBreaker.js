const lengthForBreak = 75;

export function addLineBreaks(str) {
	if (str.length > lengthForBreak) {
		let result = '';
		for (let i = 0; i < str.length; i++) {
			result += str[i];
			if ((i + 1) % lengthForBreak === 0) {
				result += '\n';
			}
		}
		return result;
	} else {
		return str;
	}
}
