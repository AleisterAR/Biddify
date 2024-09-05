import Alpine from 'alpinejs';

const Clover = {
    rule: {
        required: function (message) {
            return function (field, val) {
                return {
                    rule: 'required',
                    value: val ? false : message || `The ${field} is required`,
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
                const regex = /^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]$/;
                return {
                    rule: 'password',
                    value: val.match(regex)
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

window.Clover = Clover;
window.Alpine = Alpine;

Alpine.start();