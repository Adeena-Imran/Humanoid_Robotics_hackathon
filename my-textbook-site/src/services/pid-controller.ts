// my-textbook-site/src/services/pid-controller.ts

/**
 * Implements a basic PID (Proportional-Integral-Derivative) controller.
 */
export class PIDController {
  private kp: number;
  private ki: number;
  private kd: number;
  private previousError: number;
  private integral: number;
  private minOutput: number;
  private maxOutput: number;

  constructor(kp: number, ki: number, kd: number, minOutput: number = -Infinity, maxOutput: number = Infinity) {
    this.kp = kp;
    this.ki = ki;
    this.kd = kd;
    this.previousError = 0;
    this.integral = 0;
    this.minOutput = minOutput;
    this.maxOutput = maxOutput;
  }

  /**
   * Calculates the control output based on the current error and time step.
   * @param setpoint The desired value.
   * @param currentValue The actual measured value.
   * @param deltaTime The time elapsed since the last update.
   * @returns The control output.
   */
  public update(setpoint: number, currentValue: number, deltaTime: number): number {
    try {
      if (deltaTime === 0) return 0; // Avoid division by zero

      const error = setpoint - currentValue;

      // Proportional term
      const pTerm = this.kp * error;

      // Integral term
      this.integral += error * deltaTime;
      const iTerm = this.ki * this.integral;

      // Derivative term
      const derivative = (error - this.previousError) / deltaTime;
      const dTerm = this.kd * derivative;

      // Calculate total output
      let output = pTerm + iTerm + dTerm;

      // Clamp output to min/max limits
      output = Math.max(this.minOutput, Math.min(this.maxOutput, output));

      // Store current error for next iteration
      this.previousError = error;

      return output;
    } catch (error) {
      console.error("Error in PIDController update:", error);
      return 0; // Return a safe default
    }
  }

  /**
   * Resets the internal state of the controller (integral and previous error).
   */
  public reset(): void {
    this.integral = 0;
    this.previousError = 0;
  }
}
