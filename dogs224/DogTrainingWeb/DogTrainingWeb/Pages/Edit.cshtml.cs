using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using DogTrainingWeb.Models;
using DogTrainingWeb.Services;
using System.Threading.Tasks;

namespace DogTrainingWeb.Pages
{
    public class EditModel : PageModel
    {
        private readonly TrainingService _service;
        [BindProperty] public TrainingSchedule Schedule { get; set; }

        public EditModel(TrainingService service) => _service = service;

        public async Task<IActionResult> OnGetAsync(long id)
        {
            var item = await _service.GetScheduleByIdAsync(id);
            if (item == null) return RedirectToPage("./Manage");
            Schedule = item;
            return Page();
        }

        public async Task<IActionResult> OnPostAsync()
        {
            if (!ModelState.IsValid) return Page();
            await _service.UpdateScheduleAsync(Schedule.Id, Schedule);
            return RedirectToPage("./Manage");
        }
    }   
}

