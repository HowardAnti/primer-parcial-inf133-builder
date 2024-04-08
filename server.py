elif self.path.startswith("/pacientes/") and not query_params:
            ci = int(self.path.split("/")[2])
            response_data = self.controller.read_paciente(ci)
            HTTPDataHandler.handle_response(self, 200, response_data.__dict__)
        elif "doctor" in query_params:
            doctor = query_params["doctor"][0]
            response_data = self.controller.filter_paciente("doctor", doctor)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 202, {"message": f"ningun paciente es atendido por {doctor}"})
        elif "diagnostico" in query_params:
            diagnostico = query_params["diagnostico"][0]
            response_data = self.controller.filter_diagnostico(diagnostico)
            if response_data:
                HTTPDataHandler.handle_response(self, 200, response_data)
            else:
                HTTPDataHandler.handle_response(self, 202, {"message": f"ningun paciente fue diagnosticado con {diagnostico}"})
        