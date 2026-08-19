-- Elimina las notas del presentador del build PÚBLICO.
-- Las notas contienen la mecánica pedagógica (qué no revelar, qué observar,
-- errores a plantar). Si un estudiante presiona 'S' en el sitio, las vería.
-- Se aplica sólo vía el perfil 'publico' que corre GitHub Actions.
-- El render local (quarto render, sin perfil) las CONSERVA para clase.

function Div(el)
  if el.classes:includes("notes") then
    return {}
  end
end
