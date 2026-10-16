import Alpine from 'alpinejs';
import _hyperscript from 'hyperscript.org';
import collapse from '@alpinejs/collapse'
import persist from '@alpinejs/persist'

Alpine.plugin(collapse);
Alpine.plugin(persist);
_hyperscript.browserInit();

const Clover = {
    rule: {
        flname: function (message) {
            return function (field, val) {
                const regex =
                    /^[a-zA-Z]+(?:[' -][a-zA-Z]+){0,49}$/;
                return {
                    rule: 'flname',
                    value: val.match(regex)
                        ? false
                        : message ||
                        `The  ${field}  does not match with name format`,
                };
            };
        },
        required: function (message) {
            return function (field, val) {
                return {
                    rule: 'required',
                    value: val ? false : message || `The ${field} is required`,
                };
            };
        },
        price: function (message) {
            return function (field, val) {
                const price = parseFloat(val);
                return {
                    rule: 'price',
                    value: (!isNaN(price) && price >= 0)
                        ? false
                        : message || `The ${field} must be a positive number`,
                };
            };
        },
        optionalNumerical: function (message){
            return function (field, val) {
                if (!val) {
                    return { value: false };
                }
                
                const isPositiveNumber = /^[1-9]\d*$/;
                return {
                    rule: 'optionalNumerical',
                    value: val.match(isPositiveNumber) 
                        ? false 
                        : message || `The ${field} must be a positive number.`,
                };
            };
        },
        mail: function (message) {
            return function (field, val) {
                const regex =
                    /^[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$/;
                return {
                    rule: 'mail',
                    value: val.match(regex)
                        ? false
                        : message ||
                        `The  ${field}  does not match with mail format`,
                };
            };
        },
        password: function (message) {
            return function (field, val) {
                const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,25}$/;
                return {
                    rule: 'password',
                    value: val.match(regex)
                        ? false
                        : message ||
                        `The ${field} must have a minimum of eight characters with at least one alphabet and one number`,
                };
            };
        },
        passwordconfirm: function (message) {
            return function (field, val) {
                const password = document.querySelector('input[name="password"]').value;
                return {
                    rule: 'passwordconfirm',
                    value: val === password
                        ? false
                        : message ||
                        `The ${field} must have a minimum of eight characters with at least one alphabet and one number`,
                };
            };
        },
        string: function (message) {
            return function (field, val) {
                if (typeof val !== 'string') {
                    return {
                        rule: 'string',
                        value:
                            message ||
                            `The ${field} must be minimun minLength characters`,
                    };
                }
                return { value: false };
            };
        },
        enum: function ({ list }, message) {
            return function (field, val) {
                return {
                    rule: 'enum',
                    value: list.includes(val)
                        ? false
                        : message ||
                        `The ${field} must be include in ${list.join(',')}`,
                };
            };
        },
        termsCheck: function(message){
            return function (field, val, el) {
                return {
                    rule: 'terms',
                    value: el.checked ? false : message || `You must agree to ${field}.`,
                };
            };
        },
        number: function (message) {
            return function (field, val) {
                var regex = /^\d+$/;
                if (!val.match(regex)) {
                    return {
                        rule: 'number',
                        value: message || `The ${field} must be number`,
                    };
                }
                return { value: false };
            };
        },
        onlyWordCharacter: function (message) {
            return function (field, val) {
                var regex = /^[\w\s\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF\uFF66-\uFF9F\uFF65\uFF01-\uFF03\uFF05\uFF07-\uFF5E\u0020-\u0023\u0025\u0027-\u007E\u1000-\u109F]+$/;
                if (!val.match(regex)) {
                    return {
                        rule: 'onlyWordCharacter',
                        value: message || `The ${field} must be special charactes !#=`,
                    };
                }
                return { value: false };
            };
        },
        requiredFile: function (message) {
            return function (field, val) {
                return {
                    rule: 'requiredFile',
                    value: val.length > 0 ? false : message || `The ${field} is required`,
                };
            };
        },
        usernameLength: function (message) {
            return function (field, val) {
                var regex = /^[a-zA-Z0-9._-]{3,15}$/;
                if (!val.match(regex)) {
                    return {
                        rule: 'usernameLength',
                        value: message || `The ${field} must be special charactes !#=`,
                    };
                }
                return { value: false };
            };
        },
        usernameRestriction: function (message) {
            return function (field, val) {
                var regex = /^(?!.*[_.-]{2})[a-zA-Z0-9]+([._-][a-zA-Z0-9]+)*$/;
                if (!val.match(regex)) {
                    return {
                        rule: 'usernameRestriction',
                        value: message || `The ${field} must be special charactes !#=`,
                    };
                }
                return { value: false };
            };
        },
        requiredDropdown: function (message) {
            return function (field, val) {
                return {
                    rule: 'dropdown',
                    value: val && val !== '' && val !== 'placeholder' 
                        ? false 
                        : message || `Please select a valid option for ${field}`,
                };
            };
        },
        min({ target, amount }, message) {
            return function (field, value) {
                if (target === 'string') {
                    if (value.length < amount) {
                        return {
                            rule: 'min',
                            value:
                                message ||
                                `The ${field} must be minimum ${amount} characters.`,
                        };
                    }
                }

                if (target === 'number') {
                    if (value < parseInt(amount)) {
                        return {
                            rule: 'min',
                            value:
                                message ||
                                `The ${field} must be greater or equal ${amount}.`,
                        };
                    }
                }

                return { value: false };
            };
        },
        max({ target, amount }, message) {
            return function (field, value) {
                if (target === 'string') {
                    if (value.length > amount) {
                        return {
                            rule: 'max',
                            value:
                                message ||
                                `The ${field} must be maximum ${amount} characters.`,
                        };
                    }
                }

                if (target === 'number') {
                    if (value > parseInt(amount)) {
                        return {
                            rule: 'max',
                            value:
                                message ||
                                `The ${field} must be not be greater than ${amount}.`,
                        };
                    }
                }

                return { value: false };
            };
        },

        custom: function (message, cb) {
            return function (field, val) {
                return { rule: 'custom', value: message || cb(field, val) };
            };
        },
        object: function (attr) {
            return this.validate(attr);
        },
        file: function (message, extension = []) {
            return function (field, val) {
                return { rule: 'file', value: message || cb(field, val) };
            };
        },
        sameWith: function ({ name = [] }, message) {
            return function (field, val, el) {
                if (el) {
                    const form = el.closest('form');
                    if (!name.every((el) => form.elements[el].value === val)) {
                        return {
                            rule: 'sameWith',
                            value:
                                message ||
                                `The ${field} must be same with ${name.join(
                                    ','
                                )}`,
                        };
                    }
                }
                return { value: false };
            };
        },
        date: function ({ before, after }, message = {}) {
            return function (field, value, el) {
                if (el) {
                    const form = el.closest("form")

                    if (before) {
                        const targetDate = new Date(value).getTime()
                        const otherDate = new Date(form.elements[before].value).getTime()
                        if (targetDate > otherDate) {
                            return {
                                rule: "date.before",
                                value: message?.before || `The ${field} must be before  ${before}`
                            }
                        }
                    }

                    if (after) {
                        const targetDate = new Date(value).getTime()
                        const otherDate = new Date((form.elements[after].value)).getTime()
                        if (otherDate > targetDate) {
                            return {
                                rule: "date.after",
                                value: message?.before || `The ${field} must be after  ${after}`
                            }
                        }
                    }
                }
                return { value: false }
            }
        }
    },
    validate: function ({ rule, data }) {
        const errors = {};
        for (let k in rule) {
            for (let r of rule[k]) {
                var error = r(k, data[k]);
                if (error.value) {
                    errors[k] = error.value;
                    break;
                }
            }
        }
        return errors;
    },
    form: function ({ form, rule, messages = {}, verify = false }) {
        var data = Object.fromEntries(new FormData(form));
        var errors = this.validate({ rule, data, messages });
        if (verify) {
            for (var key in errors) {
                form.querySelector(`[clover-verify="error-${key}"]`).innerText =
                    errors[key];
            }
        }
        return {
            valid: Object.keys(errors).length ? false : true,
            data,
            errors,
        };
    },
};

document.addEventListener('alpine:init', () => {
    Alpine.directive(
        'clover-verify',
        (el, { value, modifiers, expression }, { cleanup, evaluate }) => {
            let timeout;
            const name = value || el.getAttribute('name');
            let handler = () => {
                const errors = evaluate('errors');
                if (timeout) {
                    clearTimeout(timeout);
                }
                timeout = setTimeout(function () {
                    let error;
                    for (let r of evaluate(`rule.${name}`)) {
                        const e = r(
                            name,
                            el.getAttribute('type') === 'file'
                                ? el.files
                                : el.value
                        );
                        if (e.value) {
                            error = e.value;
                            break;
                        }
                    }
                    if (error) {
                        errors[name] = error;
                    } else {
                        delete errors[name];
                    }
                }, 300);
            };

            el.addEventListener('focus', handler);
            el.addEventListener('input', handler);

            cleanup(() => {
                el.removeEventListener('focus', handler);
                el.removeEventListener('input', handler);
            });
        }
    ).before('bind');

    Alpine.directive(
        'clover-form',
        (el, { value, modifiers, expression }, { cleanup, evaluate }) => {
            const checkRule = value || 'rule';
            const handler = function (e) {
                const errors = evaluate('errors');
                e.preventDefault();
                const rule = evaluate(checkRule);
                for (let name in rule) {
                    for (let r of rule[name]) {
                        if (el.elements[name]) {
                            const e = r(
                                name,
                                el.elements[name].getAttribute('type') === 'file'
                                    ? el.elements[name].files
                                    : el.elements[name].value,
                                el.elements[name]
                            );
                            if (e.value) {
                                errors[name] = e.value;
                                break;
                            } else {
                                delete errors[name];
                            }
                        }
                    }
                }
                evaluate(expression);
            };

            el.addEventListener('submit', handler);

            cleanup(() => {
                el.removeEventListener('submit', handler);
            });
        }
    );
});

// Live clocks: any element with data-countdown="<ISO date>" or data-time-ago="<ISO date>"
// is refreshed every second, including elements swapped in later by HTMX.
const pad = (n) => String(n).padStart(2, '0');

function splitDuration(ms) {
    const s = Math.floor(ms / 1000);
    return { d: Math.floor(s / 86400), h: Math.floor((s % 86400) / 3600), m: Math.floor((s % 3600) / 60), s: s % 60 };
}

function formatCountdown(ms, style) {
    const { d, h, m, s } = splitDuration(ms);
    if (style === 'long') {
        return d > 0 ? `${d}d ${pad(h)}h ${pad(m)}m ${pad(s)}s` : `${pad(h)}h ${pad(m)}m ${pad(s)}s`;
    }
    if (d > 0) return `${d}d ${h}h left`;
    if (h > 0) return `${h}h ${pad(m)}m left`;
    return `${m}m ${pad(s)}s left`;
}

function formatTimeAgo(ms) {
    const { d, h, m, s } = splitDuration(Math.max(ms, 0));
    if (d > 0) return `${d}d ago`;
    if (h > 0) return `${h}h ago`;
    if (m > 0) return `${m}m ago`;
    return s < 5 ? 'just now' : `${s}s ago`;
}

function tickClocks() {
    const now = Date.now();
    document.querySelectorAll('[data-countdown]').forEach((el) => {
        const diff = Date.parse(el.dataset.countdown) - now;
        if (Number.isNaN(diff)) return;
        if (diff <= 0) {
            el.textContent = el.dataset.endedText || 'Ended';
            el.dataset.urgency = 'ended';
            if ('reloadOnEnd' in el.dataset && !el.dataset.reloaded) {
                el.dataset.reloaded = '1';
                setTimeout(() => window.location.reload(), 1000);
            }
            return;
        }
        el.textContent = formatCountdown(diff, el.dataset.countdownStyle);
        if (!('noUrgency' in el.dataset)) {
            el.dataset.urgency = diff < 60_000 ? 'final' : diff < 3_600_000 ? 'closing' : 'open';
        }
    });
    document.querySelectorAll('[data-time-ago]').forEach((el) => {
        el.textContent = formatTimeAgo(now - Date.parse(el.dataset.timeAgo));
    });
}

document.addEventListener('DOMContentLoaded', () => {
    tickClocks();
    setInterval(tickClocks, 1000);
});
document.addEventListener('htmx:afterSettle', tickClocks);
document.addEventListener('htmx:wsAfterMessage', tickClocks);

window.Clover = Clover;
window.Alpine = Alpine;

Alpine.start();