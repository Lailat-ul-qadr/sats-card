/**
 * @typedef {Object} User
 * @property {string} id
 * @property {string} name
 * @property {string} email
 * @property {string} phone
 * @property {string} country
 * @property {string|null} avatar
 * @property {Date} createdAt
 */

/**
 * @typedef {Object} Wallet
 * @property {number} sats - satoshis
 * @property {number} btc - bitcoin
 * @property {number} usd - USD equivalent
 * @property {number} pendingTransactions
 */

/**
 * @typedef {Object} Card
 * @property {string} cardNumber
 * @property {string} cardName
 * @property {string} holder
 * @property {string} expires
 * @property {Date} lastUsed
 * @property {string} status - 'active' | 'inactive' | 'locked'
 */

/**
 * @typedef {Object} Transaction
 * @property {string} id
 * @property {'topup'|'payment'|'spend'|'transfer'} type
 * @property {string} title
 * @property {number} amount
 * @property {string} currency - 'USD' | 'sats' | 'BTC'
 * @property {number} sats - optional satoshis
 * @property {number} usd - optional USD equivalent
 * @property {'pending'|'settled'|'failed'} status
 * @property {Date} timestamp
 * @property {string} description
 * @property {string} provider - optional mobile money provider
 * @property {string} txHash - optional transaction hash
 * @property {string} merchant - optional merchant name
 */

/**
 * @typedef {Object} Notification
 * @property {string} id
 * @property {'success'|'error'|'warning'|'info'} type
 * @property {string} title
 * @property {string} message
 * @property {Date} timestamp
 * @property {boolean} read
 */

/**
 * @typedef {Object} ExchangeRate
 * @property {string} from
 * @property {string} to
 * @property {number} rate
 * @property {Date} timestamp
 */

/**
 * @typedef {Object} MobileMoneyProvider
 * @property {string} id
 * @property {string} name
 * @property {string} logo
 * @property {string} color
 */

/**
 * @typedef {Object} AuthResponse
 * @property {boolean} success
 * @property {string} token
 * @property {User} user
 */

/**
 * @typedef {Object} ApiResponse
 * @property {boolean} success
 * @property {any} data
 * @property {string} error - optional error message
 */
