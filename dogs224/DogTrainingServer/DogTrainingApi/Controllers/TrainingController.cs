using DogTrainingApi.Models;
using Microsoft.AspNetCore.Mvc;
using System.IO;
using System.Text.Json;
using System.ComponentModel.DataAnnotations;

namespace DogTrainingApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TrainingController : ControllerBase
    {
        private const string DataFilePath = "trainingData.json";
        private static readonly object _fileLock = new object();

        // GET: api/training
        [HttpGet]
        public IActionResult GetAllSchedules()
        {
            try
            {
                var schedules = ReadSchedulesFromFile();
                return Ok(schedules);
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Error reading schedules: {ex.Message}");
            }
        }

        // GET: api/training/{id}
        [HttpGet("{id}")]
        public IActionResult GetScheduleById(long id)
        {
            try
            {
                var schedules = ReadSchedulesFromFile();
                var schedule = schedules.FirstOrDefault(s => s.Id == id);

                if (schedule == null)
                    return NotFound($"Schedule with ID {id} not found");

                return Ok(schedule);
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Error reading schedule: {ex.Message}");
            }
        }

        // POST: api/training
        [HttpPost]
        public IActionResult SaveSchedule([FromBody] TrainingSchedule schedule)
        {
            try
            {
                // Валидация
                var validationResults = ValidateTrainingSchedule(schedule);
                if (validationResults.Any())
                    return BadRequest(validationResults);

                // Генерируем ID
                schedule.Id = DateTime.Now.Ticks;

                // Читаем существующие данные
                var schedules = ReadSchedulesFromFile();

                // Добавляем новое расписание
                schedules.Add(schedule);

                // Сохраняем
                SaveSchedulesToFile(schedules);

                return Ok(new
                {
                    message = "Schedule saved successfully!",
                    id = schedule.Id
                });
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Internal server error: {ex.Message}");
            }
        }

        // PUT: api/training/{id}
        [HttpPut("{id}")]
        public IActionResult UpdateSchedule(long id, [FromBody] TrainingSchedule updatedSchedule)
        {
            try
            {
                // Валидация
                var validationResults = ValidateTrainingSchedule(updatedSchedule);
                if (validationResults.Any())
                    return BadRequest(validationResults);

                var schedules = ReadSchedulesFromFile();
                var existingSchedule = schedules.FirstOrDefault(s => s.Id == id);

                if (existingSchedule == null)
                    return NotFound($"Schedule with ID {id} not found");

                // Обновляем поля
                existingSchedule.DogName = updatedSchedule.DogName;
                existingSchedule.StartTime = updatedSchedule.StartTime;
                existingSchedule.EndTime = updatedSchedule.EndTime;
                existingSchedule.TrainingType = updatedSchedule.TrainingType;
                existingSchedule.IsCompleted = updatedSchedule.IsCompleted;

                // Сохраняем
                SaveSchedulesToFile(schedules);

                return Ok(new { message = "Schedule updated successfully!" });
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Error updating schedule: {ex.Message}");
            }
        }

        // DELETE: api/training/{id}
        [HttpDelete("{id}")]
        public IActionResult DeleteSchedule(long id)
        {
            try
            {
                var schedules = ReadSchedulesFromFile();
                var scheduleToRemove = schedules.FirstOrDefault(s => s.Id == id);

                if (scheduleToRemove == null)
                    return NotFound($"Schedule with ID {id} not found");

                schedules.Remove(scheduleToRemove);
                SaveSchedulesToFile(schedules);

                return Ok(new { message = "Schedule deleted successfully!" });
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Error deleting schedule: {ex.Message}");
            }
        }

        // GET: api/training/statistics
        [HttpGet("statistics")]
        public IActionResult GetStatistics()
        {
            try
            {
                var schedules = ReadSchedulesFromFile();

                var statistics = new
                {
                    TotalTrainings = schedules.Count,
                    CompletedTrainings = schedules.Count(s => s.IsCompleted),
                    UpcomingTrainings = schedules.Count(s => !s.IsCompleted && s.StartTime > DateTime.Now),
                    TrainingsByType = schedules
                        .GroupBy(s => s.TrainingType)
                        .Select(g => new { Type = g.Key, Count = g.Count() }),
                    TrainingsByDog = schedules
                        .GroupBy(s => s.DogName)
                        .Select(g => new { DogName = g.Key, Count = g.Count() }),
                    AverageTrainingDuration = schedules.Any() ?
                        schedules.Average(s => (s.EndTime - s.StartTime).TotalMinutes) : 0
                };

                return Ok(statistics);
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Error calculating statistics: {ex.Message}");
            }
        }

        // Вспомогательные методы
        private List<TrainingSchedule> ReadSchedulesFromFile()
        {
            lock (_fileLock)
            {
                if (!System.IO.File.Exists(DataFilePath))
                    return new List<TrainingSchedule>();

                var jsonData = System.IO.File.ReadAllText(DataFilePath);
                return JsonSerializer.Deserialize<List<TrainingSchedule>>(jsonData) ?? new List<TrainingSchedule>();
            }
        }

        private void SaveSchedulesToFile(List<TrainingSchedule> schedules)
        {
            lock (_fileLock)
            {
                var options = new JsonSerializerOptions { WriteIndented = true };
                System.IO.File.WriteAllText(DataFilePath, JsonSerializer.Serialize(schedules, options));
            }
        }

        private List<string> ValidateTrainingSchedule(TrainingSchedule schedule)
        {
            var errors = new List<string>();

            if (string.IsNullOrWhiteSpace(schedule.DogName))
                errors.Add("Dog name is required");

            if (schedule.StartTime >= schedule.EndTime)
                errors.Add("Start time must be before end time");

            if (schedule.EndTime - schedule.StartTime < TimeSpan.FromMinutes(5))
                errors.Add("Training duration must be at least 5 minutes");

            if (schedule.StartTime < DateTime.Now.AddMinutes(-5))
                errors.Add("Start time cannot be in the past");

            if (string.IsNullOrWhiteSpace(schedule.TrainingType))
                errors.Add("Training type is required");

            return errors;
        }
    }
}