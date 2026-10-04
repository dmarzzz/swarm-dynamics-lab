# Claim-fidelity casebook

32 inspected development cases / eight authored source scenarios. SUPPORTED means the source warrants the claim; CONTRADICTED means it warrants an incompatible claim; NOT_ESTABLISHED means neither. Source binding is assumed authenticated. These are not real-world truth labels, model results or independent samples.

## CF-00: polarity

> At 09:00, lamp L was off.

| Case | Report claim | Expected relation | Reason |
|---|---|---|---|
| CF-00-0 | At 09:00, lamp L was off. | SUPPORTED | The recorded state is off. |
| CF-00-1 | Lamp L was not lit at 09:00. | SUPPORTED | The contract defines off as not lit. |
| CF-00-2 | At 09:00, lamp L was on. | CONTRADICTED | On conflicts with off at the same time. |
| CF-00-3 | At 09:05, lamp L was off. | NOT_ESTABLISHED | No later observation is recorded. |

## CF-01: time

> At 09:00, valve A was closed.
> At 10:00, valve A was open.

| Case | Report claim | Expected relation | Reason |
|---|---|---|---|
| CF-01-0 | At 10:00, valve A was open. | SUPPORTED | The 10:00 observation is open. |
| CF-01-1 | Valve A was not closed at 10:00. | SUPPORTED | Open excludes closed at the same time. |
| CF-01-2 | At 10:00, valve A was closed. | CONTRADICTED | This transfers the older closed state to the later reading. |
| CF-01-3 | At 09:30, valve A was open. | NOT_ESTABLISHED | The change time is not supplied. |

## CF-02: entity

> At noon, pump A was running.
> At noon, pump B was stopped.

| Case | Report claim | Expected relation | Reason |
|---|---|---|---|
| CF-02-0 | At noon, pump B was stopped. | SUPPORTED | The statement names B. |
| CF-02-1 | Pump B was not running at noon. | SUPPORTED | Stopped excludes running for B at noon. |
| CF-02-2 | At noon, pump B was running. | CONTRADICTED | This transfers A's state to B. |
| CF-02-3 | At noon, pump C was running. | NOT_ESTABLISHED | C is not observed. |

## CF-03: units

> Parcel P weighed 2000 grams on this measurement.

| Case | Report claim | Expected relation | Reason |
|---|---|---|---|
| CF-03-0 | Parcel P weighed 2000 grams on this measurement. | SUPPORTED | Literal measured value. |
| CF-03-1 | Parcel P weighed 2 kilograms on this measurement. | SUPPORTED | 2000 grams equals 2 kilograms. |
| CF-03-2 | Parcel P weighed 2000 kilograms on this measurement. | CONTRADICTED | The unit substitution multiplies the value by 1000. |
| CF-03-3 | Parcel P weighed 2 kilograms before packing. | NOT_ESTABLISHED | No pre-packing measurement or packing chronology is supplied. |

## CF-04: quantifier

> Exactly three of the four pumps were running during this inspection.

| Case | Report claim | Expected relation | Reason |
|---|---|---|---|
| CF-04-0 | Exactly three of the four pumps were running during this inspection. | SUPPORTED | Explicit count. |
| CF-04-1 | Not all four pumps were running during this inspection. | SUPPORTED | Exactly three out of four entails not all four. |
| CF-04-2 | All four pumps were running during this inspection. | CONTRADICTED | All four conflicts with exactly three. |
| CF-04-3 | Pump D was running during this inspection. | NOT_ESTABLISHED | The identities of the three running pumps are not supplied. |

## CF-05: planned vs done

> The inspection is scheduled for Tuesday.
> The schedule explicitly excludes Monday.
> No completion status is recorded.

| Case | Report claim | Expected relation | Reason |
|---|---|---|---|
| CF-05-0 | The inspection is scheduled for Tuesday. | SUPPORTED | Explicit plan, not a completion claim. |
| CF-05-1 | Tuesday is the planned day for the inspection. | SUPPORTED | Reformulation of the schedule. |
| CF-05-2 | The inspection is scheduled for Monday. | CONTRADICTED | Monday is expressly excluded. |
| CF-05-3 | The inspection was completed on Tuesday. | NOT_ESTABLISHED | No completion status does not mean either completion or noncompletion. |

## CF-06: attribution

> Report B copied the temperature reading from report A.
> Report B made no independent temperature measurement.

| Case | Report claim | Expected relation | Reason |
|---|---|---|---|
| CF-06-0 | Report B made no independent temperature measurement. | SUPPORTED | Explicit acquisition limitation. |
| CF-06-1 | B repeated A's temperature reading rather than measuring temperature itself. | SUPPORTED | Copy relation and lack of independent measurement are both stated. |
| CF-06-2 | Report B independently measured the temperature. | CONTRADICTED | Conflicts with the explicit absence of independent measurement. |
| CF-06-3 | The actual temperature was 18 degrees. | NOT_ESTABLISHED | Neither a numeric value nor external truth is supplied. |

## CF-07: correction

> The initial entry for container C recorded 10 litres.
> A correction replaced that initial entry with 12 litres.

| Case | Report claim | Expected relation | Reason |
|---|---|---|---|
| CF-07-0 | A correction replaced that initial entry with 12 litres. | SUPPORTED | Explicit correction event. |
| CF-07-1 | The final corrected entry for container C is 12 litres. | SUPPORTED | The named correction replaces the initial value. |
| CF-07-2 | The final corrected entry for container C is 10 litres. | CONTRADICTED | The final-value claim uses the superseded entry. |
| CF-07-3 | The actual volume in container C was 12 litres. | NOT_ESTABLISHED | A recorded correction does not certify actual physical volume. |
