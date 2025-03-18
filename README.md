## SlackMe easy gateway
Project created out of necessity from Anveo VoIP SMS.
Forwarding Anveo number-destined SMS messages to a US mobile number is no longer allowed.
Therefore, the project was created as a webhook for forwarding any incoming messages to Slack.

### Needs following ENV VARs set:
- SLACK_BOT_TOKEN
- AUTH_TOKEN

#### Methods

<details>
 <summary><code>GET</code> <code><b>/sms?from={fromString}&message={messageString}?auth={authToken}</b></code> <code>(send SMS message payload to #alerts channel on Slack)</code></summary>

##### Parameters

> | name              |  type     | data type      | description                         |
> |-------------------|-----------|----------------|-------------------------------------|
> | `fromString`      |  required | string         | From Number of SMS text             |
> | `messageString`   |  required | string         | SMS text message                    |
> | `authToken`       |  required | string         | Pre-shared auth token in ENV VAR    |

##### Responses

> | http code     | content-type                      | response                                                            |
> |---------------|-----------------------------------|---------------------------------------------------------------------|
> | `200`         | `text/plain;charset=UTF-8`        | OK                                                                  |
> | `400`         | `text/plain;charset=UTF-8`        | Missing required field                                              |
> | `401`         | `text/plain;charset=UTF-8`        | AUTH TOKEN mismatch                                                 |
> | `200`         | `text/plain;charset=UTF-8`        | Server Error sending to Slack                                       |

</details>

#### Notes:
- Currently, channel is hard-coded in the method output (might make that an ENV VAR?)
- Also assumes will be behind a reverse proxy (uses WSGI ProxyFix for logging)
- Not very secure, but the sending side does not support dynamic headers or POST requests
  - Will be served by HTTPS server and will rotate token periodically
