// my-textbook-site/src/lib/physics-utils.ts

/**
 * Performs Euler integration for a simple 1D system.
 * @param currentValue The current value (e.g., position).
 * @param currentVelocity The current velocity.
 * @param acceleration The constant acceleration.
 * @param deltaTime The time step.
 * @returns The new position and velocity.
 */
export function eulerIntegrate1D(
  currentValue: number,
  currentVelocity: number,
  acceleration: number,
  deltaTime: number
): { newValue: number; newVelocity: number } {
  const newVelocity = currentVelocity + acceleration * deltaTime;
  const newValue = currentValue + currentVelocity * deltaTime; // Use currentVelocity for simple Euler
  return { newValue, newVelocity };
}

/**
 * Calculates torque from a simple proportional control law (e.g., spring-like behavior).
 * @param kp Proportional gain.
 * @param desiredPosition Desired position.
 * @param currentPosition Current position.
 * @returns Applied torque.
 */
export function calculateProportionalTorque(kp: number, desiredPosition: number, currentPosition: number): number {
  return kp * (desiredPosition - currentPosition);
}

/**
 * Simulates a single-joint system (e.g., a simple pendulum or motor).
 * Returns new position and velocity given current state, torque, and system properties.
 * This is highly simplified.
 * @param currentAngle Current angle of the joint (radians).
 * @param currentAngularVelocity Current angular velocity (rad/s).
 * @param appliedTorque The torque applied to the joint.
 * @param momentOfInertia The moment of inertia of the system.
 * @param dampingCoefficient Damping applied to the system.
 * @param deltaTime The time step.
 * @returns An object containing the new angle and new angular velocity.
 */
export function simulateSingleJointPhysics(
  currentAngle: number,
  currentAngularVelocity: number,
  appliedTorque: number,
  momentOfInertia: number,
  dampingCoefficient: number,
  deltaTime: number
): { newAngle: number; newAngularVelocity: number } {
  // Simplified: Torque = I * alpha + damping * omega
  // alpha = (Torque - damping * omega) / I
  const angularAcceleration = (appliedTorque - dampingCoefficient * currentAngularVelocity) / momentOfInertia;

  const { newValue: newAngle, newVelocity: newAngularVelocity } = eulerIntegrate1D(
    currentAngle,
    currentAngularVelocity,
    angularAcceleration,
    deltaTime
  );

  return { newAngle, newAngularVelocity };
}
