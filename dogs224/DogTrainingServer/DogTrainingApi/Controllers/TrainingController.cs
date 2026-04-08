using DogTrainingApi.Models;
using Microsoft.AspNetCore.Mvc;
using System.IO;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Linq; // Обязательно для Any() и FirstOrDefault()
using System.Collections.Generic; // Обязательно для List<>

namespace DogTrainingApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class TrainingController : ControllerBase
    {
        private const string DataFilePath = "trainingData.json";
        private static readonly object _fileLock = new object();

        [HttpGet]
        public IActionResult GetAllSchedules()
        {
            try { return Ok(ReadSchedulesFromFile()); }
            catch (Exception ex) { return StatusCode(500, $"Error: {ex.Message}"); }
        }
        [HttpGet("{id}")]
        public IActionResult GetScheduleById(long id)
        {
            try
            {
                var schedules = ReadSchedulesFromFile();
                var item = schedules.FirstOrDefault(s => s.Id == id);
                
                if (item == null) 
                    return NotFound(new { message = "Запись не найдена" });
                    
                return Ok(item);
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Ошибка при поиске: {ex.Message}");
            }
        }
        [HttpPost] // Оставили один, как и должно быть
        public IActionResult SaveSchedule([FromBody] TrainingSchedule schedule)
        {
            try
            {
                var errors = ValidateTrainingSchedule(schedule);
                if (errors.Any()) return BadRequest(errors);

                schedule.Id = DateTime.Now.Ticks;

                var schedules = ReadSchedulesFromFile();
                schedules.Add(schedule);
                SaveSchedulesToFile(schedules);

                return Ok(new { message = "Saved!" });
            }
            catch (Exception ex) 
            { 
                return StatusCode(500, ex.Message); 
            }
        }

        [HttpPut("{id}")]
        public IActionResult UpdateSchedule(long id, [FromBody] TrainingSchedule updated)
        {
            try
            {
                var errors = ValidateTrainingSchedule(updated);
                if (errors.Any()) return BadRequest(errors);

                var schedules = ReadSchedulesFromFile();
                var existing = schedules.FirstOrDefault(s => s.Id == id);
                if (existing == null) return NotFound();

                existing.StartTime = updated.StartTime;
                existing.TrainingType = updated.TrainingType;

                SaveSchedulesToFile(schedules);
                return Ok(new { message = "Schedule updated successfully!" });
            }
            catch (Exception ex)
            {
                return StatusCode(500, $"Error updating schedule: {ex.Message}");
            }
        }

        [HttpDelete("{id}")]
        public IActionResult DeleteSchedule(long id)
        {
            var schedules = ReadSchedulesFromFile();
            var item = schedules.FirstOrDefault(s => s.Id == id);
            if (item == null) return NotFound();

            schedules.Remove(item);
            SaveSchedulesToFile(schedules);
            return Ok(new { message = "Deleted!" });
        }

        private List<string> ValidateTrainingSchedule(TrainingSchedule schedule)
        {
            var errors = new List<string>();

            if (string.IsNullOrWhiteSpace(schedule.StartTime))
            {
                errors.Add("Time is required");
            }
            // Упростили запись, так как using Regex уже есть вверху
            else if (!Regex.IsMatch(schedule.StartTime, @"^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"))
            {
                errors.Add("Invalid time format. Use HH:mm");
            }

            return errors;
        }

        private List<TrainingSchedule> ReadSchedulesFromFile()
        {
            lock (_fileLock)
            {
                if (!System.IO.File.Exists(DataFilePath)) return new List<TrainingSchedule>();
                var json = System.IO.File.ReadAllText(DataFilePath);
                return JsonSerializer.Deserialize<List<TrainingSchedule>>(json) ?? new List<TrainingSchedule>();
            }
        }

        private void SaveSchedulesToFile(List<TrainingSchedule> schedules)
        {
            lock (_fileLock)
            {
                var json = JsonSerializer.Serialize(schedules, new JsonSerializerOptions { WriteIndented = true });
                System.IO.File.WriteAllText(DataFilePath, json);
            }
        }
    }
}