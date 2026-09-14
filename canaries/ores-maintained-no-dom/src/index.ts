import type {
  LeaseAbortListener,
  LeaseAbortListenerOptions,
  LeaseAbortSignal,
  MaintainedXactGuarded,
} from "@oresoftware/locks-and-leases";

const listener: LeaseAbortListener = () => undefined;
const options: LeaseAbortListenerOptions = { once: true };

declare const signal: LeaseAbortSignal;
signal.addEventListener("abort", listener, options);
signal.removeEventListener("abort", listener, options);

export function consumeMaintainedGuard(guard: MaintainedXactGuarded): unknown {
  if (guard.signal.aborted) return guard.signal.reason;
  guard.signal.throwIfAborted();
  return guard.grant.fencingToken;
}
