from ortools.init.python import init
from ortools.linear_solver import pywraplp


def main():
    print("Google OR-Tools version:", init.OrToolsVersion.version_string())

    # Crear el solver con GLOP
    solver = pywraplp.Solver.CreateSolver("GLOP")
    if not solver:
        print("No se pudo crear el solver GLOP")
        return

    # Variables de decisión
    x_var = solver.NumVar(0, 2, "x")  # 0 ≤ x ≤ 2
    y_var = solver.NumVar(0, 3, "y")  # 0 ≤ y ≤ 3

    print("Número de variables =", solver.NumVariables())

    infinity = solver.infinity()

    # Restricción 1: 2x + y ≤ 3
    c1 = solver.Constraint(-infinity, 3, "ct1")
    c1.SetCoefficient(x_var, 2)
    c1.SetCoefficient(y_var, 1)

    # Restricción 2: x + 2y ≤ 4
    c2 = solver.Constraint(-infinity, 4, "ct2")
    c2.SetCoefficient(x_var, 1)
    c2.SetCoefficient(y_var, 2)

    print("Número de restricciones =", solver.NumConstraints())

    # Nueva función objetivo: 5x + 2y
    objective = solver.Objective()
    objective.SetCoefficient(x_var, 5)
    objective.SetCoefficient(y_var, 2)
    objective.SetMaximization()

    print(f"Resolviendo con {solver.SolverVersion()}")
    result_status = solver.Solve()

    print(f"Estado: {result_status}")
    if result_status != pywraplp.Solver.OPTIMAL:
        print("¡El problema no tiene una solución óptima!")
        return

    print("Solución:")
    print("Valor de la función objetivo =", objective.Value())
    print("x =", x_var.solution_value())
    print("y =", y_var.solution_value())


if __name__ == "__main__":
    init.CppBridge.init_logging("problema_modificado.py")
    cpp_flags = init.CppFlags()
    cpp_flags.stderrthreshold = True
    cpp_flags.log_prefix = False
    init.CppBridge.set_flags(cpp_flags)
    main()
