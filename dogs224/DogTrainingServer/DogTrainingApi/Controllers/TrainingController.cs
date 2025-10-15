using DogTrainingApi.Models;
using Microsoft.AspNetCore.Mvc;
using System.IO;
using System.Text.Json;

namespace DogTrainingApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TrainingController : ControllerBase
    {
        private const string DataFilePath = "trainingData.json";
        
        [HttpPost]
        public IActionResult SaveSchedule([FromBody] TrainingSchedule schedule)
        {
            try
            {
                // Генерируем уникальный ID
                schedule.Id = DateTime.Now.Ticks; 
                
                // Читаем существующие данные
                List<TrainingSchedule> schedules = new();
                if (System.IO.File.Exists(DataFilePath))
                {
                    var jsonData = System.IO.File.ReadAllText(DataFilePath);
                    schedules = JsonSerializer.Deserialize<List<TrainingSchedule>>(jsonData) ?? new();
                }
                
                // Добавляем новое расписание
                schedules.Add(schedule);
                
                // Сохраняем в файл
                var options = new JsonSerializerOptions { WriteIndented = true };
                System.IO.File.WriteAllText(DataFilePath, JsonSerializer.Serialize(schedules, options));
                
                return Ok(new { message = "Schedule saved successfully!" });
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Internal server error: {ex.Message}");
            }
        }
    }
}